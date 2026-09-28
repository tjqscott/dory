"""Stop: if this session changed wiki/, lint it and refuse to stop until it is clean."""

import os
import sys
import json
import pathlib
import subprocess

sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import wiki_tree  # noqa: E402

data = json.load(sys.stdin)
if data.get("stop_hook_active"):
    sys.exit(0)  # already sent back once; don't loop

project = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")
wiki = project / "wiki"
if not (wiki / "index.md").exists():
    sys.exit(0)
try:
    changed = subprocess.run(["git", "status", "--porcelain", "--", "wiki"], cwd=project,
                             capture_output=True, text=True, timeout=10).stdout.strip()
except (OSError, subprocess.TimeoutExpired):
    changed = "unknown"  # no git: lint anyway
if not changed:
    sys.exit(0)

problems, _ = wiki_tree.lint(wiki)
if problems:
    print("The wiki lint found problems. Fix them before finishing (AGENTS.md V):\n"
          + "\n".join(f"- {p}" for p in problems), file=sys.stderr)
    sys.exit(2)
