"""Statusline: show the model and five-hour usage, and save the rate limits
where Dory's prompt hook can read them. Hooks do not receive rate limits;
only the statusline does."""

import sys
import json
import time
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

data = json.load(sys.stdin)
limits = data.get("rate_limits")
if limits:
    out = pathlib.Path.home() / ".claude" / "dory-usage.json"
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps({"written_at": time.time(), "rate_limits": limits}), encoding="utf-8")
    tmp.replace(out)

five = (limits or {}).get("five_hour", {}).get("used_percentage")
model = (data.get("model") or {}).get("display_name", "")
print(" · ".join(x for x in (model, f"5h {five:.0f}%" if five is not None else "") if x))
