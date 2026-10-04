#!/usr/bin/env python3
"""Can a local model keep project notes? Three ways to record one changed fact.

    python3 bench/notes_bench.py --models qwen3:8b            # run (needs Ollama)
    python3 bench/notes_bench.py --models a b --trials 30
    python3 bench/notes_bench.py --selftest                    # check the scorers, no model

Each trial gives the model the same notes and the same change, and asks for it as:
  rewrite  the whole notes file back, with one line changed
  patch    a SEARCH/REPLACE block for that one line
  append   a Dory post that replaces the old fact

A trial passes when the notes end up exactly right. Each arm gets one retry with
the error it would see in real use. Results land in bench/results/.
"""

import re
import sys
import json
import random
import pathlib
import argparse
import urllib.request

OLLAMA = "http://localhost:11434/api/chat"
OUT = pathlib.Path(__file__).parent / "results"
ARMS = ("rewrite", "patch", "append")
SIZES = (20, 60, 150)  # facts in the notes

MODULES = ["auth", "billing", "search", "export", "sync", "uploads", "email", "api", "admin", "reports",
           "cache", "queue", "logging", "backup", "onboarding"]
ASPECTS = {
    "Storage": ["SQLite", "Postgres", "Redis", "flat JSON files", "DynamoDB"],
    "Retry policy": ["3 tries with backoff", "no retries", "5 tries, fixed delay", "retry once"],
    "Timeout": ["5 seconds", "30 seconds", "2 minutes", "none"],
    "Owner": ["Priya", "Marcus", "Ana", "Tom", "the platform team"],
    "Format": ["JSON", "CSV", "Parquet", "protobuf"],
    "Rate limit": ["60 per minute", "10 per second", "1000 per day", "unlimited"],
    "Auth": ["session cookie", "API key", "OAuth", "signed URL"],
    "Deploys": ["on merge", "nightly", "by hand", "weekly"],
    "Test level": ["unit only", "unit and integration", "end to end", "none yet"],
    "Logging": ["errors only", "every request", "sampled at 1%", "off"],
}
REASONS = ["the old choice fell over under load", "it halves the cost", "the team already runs it",
           "the last incident traced back here", "a customer needs it", "it removes a dependency"]

FORMAT = """=== dory post ===
title: <short title>
page: <lowercase-slug>
replaces: <post ids separated by commas; omit if none>
---
<markdown body>
=== end ==="""


def make_case(n_facts, rng):
    """A set of facts, one to change, and what the notes must say afterwards."""
    keys = [(m, a) for m in MODULES for a in ASPECTS]
    rng.shuffle(keys)
    facts = [{"id": i + 1, "module": m, "aspect": a, "value": rng.choice(ASPECTS[a])}
             for i, (m, a) in enumerate(sorted(keys[:n_facts]))]
    target = rng.choice(facts)
    new_value = rng.choice([v for v in ASPECTS[target["aspect"]] if v != target["value"]])
    return facts, target, new_value, rng.choice(REASONS)


def line(f, value=None, reason=None):
    return f"- **{f['aspect']}:** {value or f['value']}" + (f", because {reason}." if reason else ".")


def notes_file(facts, target=None, new_line=None):
    out, module = ["# Project notes"], None
    for f in facts:
        if f["module"] != module:
            module = f["module"]
            out += ["", f"## {module}"]
        out.append(new_line if f is target else line(f))
    return "\n".join(out) + "\n"


def notes_posts(facts):
    return "\n\n".join(f"#### #{f['id']} {f['aspect']} (page: {f['module']})\n{line(f)}" for f in facts)


def prompts(arm, facts, target, new_line):
    change = (f"In the `{target['module']}` section, the **{target['aspect']}** line is out of date. "
              f"It must now read exactly:\n{new_line}")
    if arm == "rewrite":
        return (f"Here are the project notes:\n\n{notes_file(facts)}\n{change}\n\n"
                "Reply with the complete updated notes file and nothing else. Change only that line.")
    if arm == "patch":
        return (f"Here are the project notes:\n\n{notes_file(facts)}\n{change}\n\n"
                "Reply with one edit block and nothing else, in exactly this form:\n"
                "<<<<<<< SEARCH\n<the exact current text>\n=======\n<the new text>\n>>>>>>> REPLACE\n"
                "The SEARCH text must match exactly one place in the file. The same line can appear in several "
                "sections, so include the section heading or neighbouring lines when it does.")
    return (f"Here are the project notes, one fact per post, each with an id:\n\n{notes_posts(facts)}\n\n{change}\n\n"
            "Never edit an old post. Reply with one new post that replaces the outdated one, and nothing else, "
            f"in exactly this form:\n\n{FORMAT}\n\nThe body is the new line. `page` is the section name. "
            "`replaces` is the id of the post it supersedes.")


def clean(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
    fence = re.search(r"```[a-zA-Z]*\n(.*?)```", text, flags=re.S)
    return (fence.group(1) if fence and len(fence.group(1)) > len(text) / 2 else text).strip()


def same(a, b):
    return [l.rstrip() for l in a.strip().splitlines()] == [l.rstrip() for l in b.strip().splitlines()]


def score(arm, reply, facts, target, new_line):
    """Return (passed, message the model would get back on failure)."""
    want = notes_file(facts, target, new_line)
    reply = clean(reply)
    if arm == "rewrite":
        if same(reply, want):
            return True, ""
        got, exp = reply.strip().splitlines(), want.strip().splitlines()
        return False, (f"The file you returned is wrong: it has {len(got)} lines and should have {len(exp)}, "
                       "or lines other than the target changed. Return the complete file with only that one line changed.")
    if arm == "patch":
        m = re.search(r"<{5,} SEARCH\n(.*?)\n={5,}\n(.*?)\n>{5,} REPLACE", reply, flags=re.S)
        if not m:
            return False, "No valid SEARCH/REPLACE block found. Reply with exactly one block in the required form."
        original = notes_file(facts)
        if original.count(m.group(1)) != 1:
            return False, "The SEARCH text must match exactly one place in the file. Copy the current line exactly."
        return (True, "") if same(original.replace(m.group(1), m.group(2)), want) else (
            False, "The block applied, but the result is not the requested change. Replace only that line with the exact new line.")
    m = re.search(r"=== dory post ===\n(.*?)\n---\n(.*?)\n=== end ===", reply, flags=re.S)
    if not m:
        return False, "Dory rejected your post: missing the `=== dory post ===` header, the `---` line or the `=== end ===` line."
    head = dict(re.findall(r"^\s*([a-z]+)\s*:\s*(.*?)\s*$", m.group(1), flags=re.M))
    if not head.get("title"):
        return False, 'Dory rejected your post: missing "title:".'
    if head.get("page") != target["module"]:
        return False, f'Dory rejected your post: "page:" must be the section name, `{target["module"]}`.'
    if head.get("replaces", "").lstrip("#") != str(target["id"]):
        return False, 'Dory rejected your post: "replaces:" must be the id of the one outdated post.'
    return (True, "") if m.group(2).strip() == new_line else (False, "Dory rejected your post: the body must be exactly the new line.")


def ask(model, messages, n_facts, temperature):
    options = {"num_ctx": 8192 if n_facts <= 60 else 16384, "num_predict": 60 * n_facts + 400}
    if temperature is not None:
        options["temperature"] = temperature
    body = json.dumps({"model": model, "messages": messages, "stream": False, "options": options}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        data = json.load(r)
    return data["message"]["content"], data.get("eval_count", 0)


def run(model, trials, temperature):
    records, total, done = [], trials * len(SIZES) * len(ARMS), 0
    for n in SIZES:
        for t in range(trials):
            facts, target, new_value, reason = make_case(n, random.Random(f"{n}-{t}"))
            new_line = line(target, new_value, reason)
            for arm in ARMS:
                messages = [{"role": "user", "content": prompts(arm, facts, target, new_line)}]
                reply, tokens = ask(model, messages, n, temperature)
                first, error = score(arm, reply, facts, target, new_line)
                retry = first
                if not first:
                    messages += [{"role": "assistant", "content": reply}, {"role": "user", "content": error}]
                    reply, more = ask(model, messages, n, temperature)
                    retry, tokens = score(arm, reply, facts, target, new_line)[0], tokens + more
                records.append({"facts": n, "trial": t, "arm": arm, "first": first, "retry": retry, "tokens": tokens})
                done += 1
                print(f"\r{model.ljust(24)} {done}/{total}  {arm.ljust(8)} facts={str(n).ljust(4)}", end="", flush=True)
    print()
    return records


def summarise(records):
    rows = []
    for n in SIZES:
        for arm in ARMS:
            cell = [r for r in records if r["facts"] == n and r["arm"] == arm]
            if cell:
                rows.append({"facts": n, "arm": arm, "trials": len(cell),
                             "first": sum(r["first"] for r in cell) / len(cell),
                             "retry": sum(r["retry"] for r in cell) / len(cell),
                             "tokens": sum(r["tokens"] for r in cell) / len(cell)})
    return rows


def chart(results):
    """One dark SVG: for each model, pass rate after one retry by notes size, three bars per size."""
    colours = {"rewrite": "#f2a7c3", "patch": "#8a8f98", "append": "#9fd3ea"}
    w, panel_h, left, top = 900, 250, 70, 60
    h = top + panel_h * len(results) + 30
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="system-ui, sans-serif">',
         f'<rect width="{w}" height="{h}" fill="#111"/>',
         '<text x="70" y="34" fill="#eee" font-size="20" font-weight="700">Notes correct after one retry</text>']
    for i, arm in enumerate(ARMS):
        s.append(f'<rect x="{480 + i * 130}" y="20" width="14" height="14" fill="{colours[arm]}"/>'
                 f'<text x="{500 + i * 130}" y="32" fill="#bbb" font-size="14">{arm}</text>')
    for p, (model, rows) in enumerate(results.items()):
        y0, plot_h = top + p * panel_h, panel_h - 100
        s.append(f'<text x="{left}" y="{y0 + 16}" fill="#eee" font-size="15" font-weight="600">{model}</text>')
        s.append(f'<line x1="{left}" y1="{y0 + 54 + plot_h}" x2="{w - 30}" y2="{y0 + 54 + plot_h}" stroke="#333"/>')
        for g, n in enumerate(SIZES):
            gx = left + 40 + g * 260
            for b, arm in enumerate(ARMS):
                rate = next((r["retry"] for r in rows if r["facts"] == n and r["arm"] == arm), 0)
                bh = rate * plot_h
                x = gx + b * 62
                s.append(f'<rect x="{x}" y="{y0 + 54 + plot_h - bh:.1f}" width="54" height="{bh:.1f}" fill="{colours[arm]}"/>')
                s.append(f'<text x="{x + 27}" y="{y0 + 48 + plot_h - bh:.1f}" fill="#eee" font-size="13" text-anchor="middle">{rate:.0%}</text>')
            s.append(f'<text x="{gx + 89}" y="{y0 + 74 + plot_h}" fill="#888" font-size="13" text-anchor="middle">{n} facts</text>')
    return "\n".join(s) + "\n</svg>\n"


def selftest():
    facts, target, new_value, reason = make_case(20, random.Random(1))
    new_line = line(target, new_value, reason)
    good = {"rewrite": notes_file(facts, target, new_line),
            "patch": f"<<<<<<< SEARCH\n{line(target)}\n=======\n{new_line}\n>>>>>>> REPLACE",
            "append": f"=== dory post ===\ntitle: {target['aspect']} changed\npage: {target['module']}\nreplaces: {target['id']}\n---\n{new_line}\n=== end ==="}
    bad = {"rewrite": notes_file(facts, target, new_line).replace("## ", "### ", 1),
           "patch": f"<<<<<<< SEARCH\n- not a real line\n=======\n{new_line}\n>>>>>>> REPLACE",
           "append": good["append"].replace(f"replaces: {target['id']}", "replaces: 9999")}
    for arm in ARMS:
        assert score(arm, good[arm], facts, target, new_line)[0], f"{arm}: a correct reply failed"
        assert score(arm, "Sure! Here you go:\n```\n" + good[arm] + "\n```", facts, target, new_line)[0], f"{arm}: a fenced reply failed"
        assert score(arm, "<think>hmm</think>\n" + good[arm], facts, target, new_line)[0], f"{arm}: a reply after thinking failed"
        passed, message = score(arm, bad[arm], facts, target, new_line)
        assert not passed and message, f"{arm}: a wrong reply passed"
    assert chart({"model": summarise([{"facts": 20, "arm": a, "first": True, "retry": True, "tokens": 1} for a in ARMS])}).startswith("<svg")
    print("selftest passed: each arm accepts a correct reply and rejects a wrong one")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--models", nargs="+", help="Ollama model tags, as shown by `ollama list`")
    ap.add_argument("--trials", type=int, default=20, help="trials per notes size and arm (default 20)")
    ap.add_argument("--temperature", type=float, help="default: the model's own")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.models:
        ap.error("--models is required")
    OUT.mkdir(exist_ok=True)
    for model in args.models:
        records = run(model, args.trials, args.temperature)
        (OUT / (re.sub(r"[^A-Za-z0-9.-]", "_", model) + ".json")).write_text(
            json.dumps({"model": model, "trials": args.trials, "temperature": args.temperature,
                        "summary": summarise(records), "records": records}, indent=1))
    results = {}
    for path in sorted(OUT.glob("*.json")):
        saved = json.loads(path.read_text())
        results[saved["model"]] = saved["summary"]
    (OUT / "chart.svg").write_text(chart(results))
    print("\n" + "model".ljust(24) + "facts".ljust(7) + "arm".ljust(9) + "first try".ljust(11) + "after retry".ljust(13) + "tokens out")
    for model, rows in results.items():
        for r in rows:
            print(model.ljust(24) + str(r["facts"]).ljust(7) + r["arm"].ljust(9) + f"{r['first']:.0%}".ljust(11)
                  + f"{r['retry']:.0%}".ljust(13) + f"{r['tokens']:.0f}")
    print(f"\nchart: {OUT / 'chart.svg'}")


if __name__ == "__main__":
    main()
