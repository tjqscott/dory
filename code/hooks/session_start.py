"""SessionStart: load Dory's directives, the wiki index and the taskboard's Now list."""

import os
import re
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PLUGIN = pathlib.Path(__file__).resolve().parents[2]
WIKI = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "wiki"

# Section IV is for browser chats, where there is no repo.
agents = (PLUGIN / "AGENTS.md").read_text(encoding="utf-8")
out = ["# Dory directives"] + [s.strip() for s in re.split(r"(?m)^(?=## )", agents) if re.match(r"## (I|II|III|V|VI)\. ", s)]

index = WIKI / "index.md"
if index.exists():
    out.append("# Wiki index (wiki/index.md)\n\n" + index.read_text(encoding="utf-8").strip())
    tickets = WIKI / "tickets.md"
    now = re.search(r"(?ms)^## Now\n(.*?)(?=^## |\Z)", tickets.read_text(encoding="utf-8")) if tickets.exists() else None
    if now and now.group(1).strip():
        out.append("# Taskboard, Now (wiki/tickets.md)\n\n" + now.group(1).strip())
else:
    out.append("This repo has no wiki/ yet. Offer /dory:init when real work starts.")
print("\n\n".join(out))
