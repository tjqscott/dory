#!/usr/bin/env python3
"""
dory_init.py — one-shot bootstrap for a Dory-managed project.

Creates .dory/{agents.md,history/}, CHANGELOG.md, and two context
snapshots (.dory/tree.md, .dory/probe.md), then deletes itself.

Usage: python3 dory_init.py
"""
import os
from datetime import datetime, timezone

ROOT = os.getcwd()
DORY_DIR = os.path.join(ROOT, ".dory")
HISTORY_DIR = os.path.join(DORY_DIR, "history")
AGENTS_MD = os.path.join(DORY_DIR, "agents.md")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
TREE_FILE = os.path.join(DORY_DIR, "tree.md")
PROBE_FILE = os.path.join(DORY_DIR, "probe.md")

DEFAULT_AGENTS_MD = """# Operational Directives

## I. Core Behaviors
* **Intent-First:** Prioritize structural goals and system architecture over shallow literal text interpretations.
* **Zero-Padding:** Do not generate conversational wrapping, introductions, or summaries. Output raw code blocks directly.
* **Decomposition:** For complex tasks, explicitly state the execution phase: `[PLANNING]` -> `[IMPLEMENTING]` -> `[TESTING]` -> `[ITERATING]`. Optional for isolated, minor requests.

## II. Tactical Engineering
* **Minimalism:** Write clean, flat code. Omit redundant try-catch blocks, unnecessary helper abstractions, and obvious comments.
* **Terminal Aesthetics:** Format outputs for clean real-time feedback. Use left/right justification (`.ljust()`), self-flushing prints (`flush=True`), and single-line progress indicators.
* **Verification Loop:** Run terminal probe scripts (`ls`, `grep`, `head`) to check directory structures and verify state before writing code.

## III. Vault Protocols
* **Append-Only Ledger:** Upon task completion, provide a single-line entry for `CHANGELOG.md` using the format: *Action + Component + Reason*. Exclude transient fixes.
* **Artifact Vaulting:** Conclude successful sessions by generating a markdown summary and clean code variants saved to `history/`.
* **Token Gating:** Append a cumulative token estimate at the end of every response (e.g., `[Cumulative Session Tokens: ~8,500]`).
* **Iteration Limits:** If `[TESTING]` fails, enter `[ITERATING]` with exact error logs. If token metrics indicate saturation, vault the failing state and recommend a session reset.
"""

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".dory", "venv", ".venv", "dist", "build"}
PROBE_EXTENSIONS = (".csv", ".json")
HEAD_LINES = 8
MAX_LINE_LEN = 200
MAX_LINE_BYTES = 2000       # hard cap read per line, before truncating for display
MAX_PROBE_FILES = 5

# Substrings (case-insensitive) that mark a file as too sensitive to preview.
SENSITIVE_PATTERNS = [
    ".env", "secret", "credential", "password", "passwd",
    "token", "apikey", "api_key", "private_key", "id_rsa", ".pem",
]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def is_sensitive(filename):
    lower = filename.lower()
    return any(pat in lower for pat in SENSITIVE_PATTERNS)


def bootstrap():
    created = []
    if os.path.isdir(DORY_DIR):
        print(f"[skip] {DORY_DIR} already exists — not touching history/ or agents.md")
    else:
        os.makedirs(HISTORY_DIR)
        with open(AGENTS_MD, "w") as f:
            f.write(DEFAULT_AGENTS_MD)
        created += [DORY_DIR, HISTORY_DIR, AGENTS_MD]

    if os.path.isfile(CHANGELOG):
        print(f"[skip] {CHANGELOG} already exists — not overwriting")
    else:
        with open(CHANGELOG, "w") as f:
            f.write("# Changelog\n\n")
        created.append(CHANGELOG)

    for path in created:
        print(f"[created] {os.path.relpath(path, ROOT)}")


def build_tree(start, prefix=""):
    lines = []
    try:
        entries = sorted(e for e in os.listdir(start) if e not in IGNORE_DIRS and not e.startswith("."))
    except PermissionError:
        return lines
    for i, entry in enumerate(entries):
        path = os.path.join(start, entry)
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry)
        if os.path.isdir(path):
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(build_tree(path, prefix + extension))
    return lines


def write_tree_file():
    lines = [os.path.basename(ROOT) or ROOT] + build_tree(ROOT)
    with open(TREE_FILE, "w") as f:
        f.write("# Repository Tree\n\n")
        f.write(f"Generated: {now()}\n")
        f.write("Ignored: " + ", ".join(sorted(IGNORE_DIRS)) + " (and any dotfiles)\n\n")
        f.write("```text\n")
        f.write("\n".join(lines))
        f.write("\n```\n")
    print(f"[created] {os.path.relpath(TREE_FILE, ROOT)}")


def find_probe_targets():
    found, skipped = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for fname in filenames:
            if not fname.endswith(PROBE_EXTENSIONS):
                continue
            path = os.path.join(dirpath, fname)
            if is_sensitive(fname):
                skipped.append(os.path.relpath(path, ROOT))
            else:
                found.append(path)
        if len(found) >= MAX_PROBE_FILES:
            break
    return found[:MAX_PROBE_FILES], skipped


def head_lines(path):
    lines = []
    with open(path, "r", errors="replace") as f:
        for i, raw in enumerate(f):
            if i >= HEAD_LINES:
                break
            chunk = raw[:MAX_LINE_BYTES].rstrip("\n")
            if len(chunk) > MAX_LINE_LEN:
                chunk = chunk[:MAX_LINE_LEN] + " ...[truncated]"
            lines.append(chunk)
    return lines


def write_probe_file():
    targets, skipped = find_probe_targets()
    with open(PROBE_FILE, "w") as f:
        f.write("# Data File Probes\n\n")
        f.write(f"Generated: {now()}\n")
        f.write(f"First {HEAD_LINES} lines of up to {MAX_PROBE_FILES} .csv/.json files.\n\n")

        if not targets:
            f.write("_No .csv/.json files found to probe._\n\n")
        for path in targets:
            rel = os.path.relpath(path, ROOT)
            f.write(f"## {rel}\n\n")
            try:
                lines = head_lines(path)
                f.write("```text\n" + "\n".join(lines) + "\n```\n\n")
            except OSError as e:
                f.write(f"_Error reading file: {e}_\n\n")

        if skipped:
            f.write("---\n\n")
            f.write("**Skipped (filename matched a sensitive pattern, not previewed):**\n\n")
            for rel in skipped:
                f.write(f"- `{rel}`\n")
    print(f"[created] {os.path.relpath(PROBE_FILE, ROOT)}")
    if skipped:
        print(f"[skipped {len(skipped)} sensitive file(s), see probe.md]")


def self_delete():
    try:
        os.remove(__file__)
        print(f"[self-deleted] {__file__}")
    except OSError as e:
        print(f"[warning] could not self-delete ({e}) — remove manually: {__file__}")


if __name__ == "__main__":
    print("=== Dory Init ===")
    bootstrap()
    write_tree_file()
    write_probe_file()
    self_delete()
    print("=== Done ===")
