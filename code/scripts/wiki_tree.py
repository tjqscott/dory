"""Draw a Dory wiki's tree from its links, and lint it.

    python wiki_tree.py [wiki_dir]           # tree + problems; exit 1 if any
    python wiki_tree.py [wiki_dir] --write   # also refresh the gen fence in index.md

The tree is read out of the links, so it cannot disagree with the pages.
`index.md` is the root. A page is drawn under the nearest page that links it;
any other link into it is a problem, except a child linking back to its
parent. Links under a `## Related` heading, and links between pages of one
subtree whose hub contains `<!-- dory:frozen -->`, are annotations, not
hierarchy.
"""

import re
import sys
import pathlib
import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")
FENCE = re.compile(r"(<!-- gen: wiki_tree\.py[^>]*-->\n).*?(\n?<!-- /gen -->)", re.S)
FROZEN = "<!-- dory:frozen -->"


def read(wiki):
    paths = {p.relative_to(wiki).with_suffix("").as_posix(): p for p in sorted(wiki.rglob("*.md"))}
    by_name = defaultdict(list)
    for k in paths:
        by_name[k.rsplit("/", 1)[-1]].append(k)

    down = defaultdict(list)     # page -> pages it links as children
    related = defaultdict(list)  # page -> pages linked under ## Related
    parents = defaultdict(list)  # page -> pages linking it as a child
    broken, frozen = [], set()

    for k, p in paths.items():
        text = p.read_text(encoding="utf-8", errors="replace")
        if FROZEN in text:
            frozen.add(k)
        # A link inside code is a reference, not an edge.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`]*`", "", text)
        cut = re.search(r"^##+\s*Related\s*$", text, re.M)
        related_from = cut.start() if cut else len(text)
        found = [(m.start(), m.group(1).strip(), True) for m in WIKILINK.finditer(text)]
        found += [(m.start(), m.group(1), False) for m in MDLINK.finditer(text) if "://" not in m.group(1)]
        seen = set()
        for pos, raw, wikilink in sorted(found):
            if wikilink:
                name = raw.removesuffix(".md")
                cands = [name] if name in paths else by_name.get(name.rsplit("/", 1)[-1], [])
                target = cands[0] if len(cands) == 1 else None
            else:
                try:
                    target = (p.parent / raw).resolve().relative_to(wiki.resolve()).with_suffix("").as_posix()
                except ValueError:
                    continue  # points outside the wiki
            if target not in paths:
                broken.append(f"{k} -> {raw}")
                continue
            if target == k or target in seen:
                continue
            seen.add(target)
            if pos >= related_from:
                related[k].append(target)
            else:
                down[k].append(target)
                parents[target].append(k)
    return paths, down, related, parents, broken, frozen


def tree(down):
    # Breadth-first, so the page nearest the root owns each child.
    kids, parent, reached, queue = defaultdict(list), {}, {"index"}, ["index"]
    while queue:
        node = queue.pop(0)
        for c in down.get(node, []):
            if c not in reached:
                reached.add(c)
                parent[c] = node
                kids[node].append(c)
                queue.append(c)
    lines = []

    def walk(node, prefix="", last=True, depth=0):
        if depth:
            lines.append(f"{prefix}{'└── ' if last else '├── '}{node}")
            prefix += "    " if last else "│   "
        else:
            lines.append(node)
        for i, c in enumerate(kids[node]):
            walk(c, prefix, i == len(kids[node]) - 1, depth + 1)

    walk("index")
    return lines, reached, parent, kids


def lint(wiki):
    """Return (problems, tree lines) for the wiki at `wiki`."""
    paths, down, related, parents, broken, frozen = read(wiki)
    if "index" not in paths:
        return [f"no index.md in {wiki}"], []
    lines, reached, parent, kids = tree(down)

    def frozen_hub(k):
        while k is not None:
            if k in frozen:
                return k
            k = parent.get(k)
        return None

    def same_archive(a, b):
        return frozen_hub(a) is not None and frozen_hub(a) == frozen_hub(b)

    problems = [f"orphan, nothing links it: {k}" for k in paths if k != "index" and k not in parents]
    problems += [f"unreachable from index: {k}" for k in paths if k not in reached and k in parents]
    for c, ps in parents.items():
        stray = [p for p in ps if p != parent.get(c) and p not in kids.get(c, []) and not same_archive(c, p)]
        if stray:
            problems.append(f"linked from outside its branch: {c} <- {', '.join(stray)}")
    problems += [f"Related link outside a frozen subtree: {s} -> {t}"
                 for s, ts in related.items() for t in ts if not same_archive(s, t)]
    problems += [f"broken link: {b}" for b in broken]
    return sorted(problems), lines


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    wiki = pathlib.Path(args[0] if args else "wiki")
    problems, lines = lint(wiki)
    print("\n".join(lines))
    print(f"\n{len(problems)} problem(s)")
    for p in problems:
        print(f"  {p}")
    if "--write" in sys.argv and lines:
        index = wiki / "index.md"
        text = index.read_text(encoding="utf-8")
        stamp = datetime.date.today().isoformat()
        body = "\n".join(lines)
        new, n = FENCE.subn(lambda m: f"<!-- gen: wiki_tree.py — {stamp} -->\n```text\n{body}\n```{m.group(2)}", text)
        if n:
            index.write_text(new, encoding="utf-8")
            print("\nwrote the tree into index.md")
        else:
            print("\nno gen fence in index.md")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
