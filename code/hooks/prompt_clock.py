"""UserPromptSubmit: put the time and the rate-limit usage into context as one [dory] line."""

import sys
import json
import time
import pathlib
import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

USAGE = pathlib.Path.home() / ".claude" / "dory-usage.json"
STALE = 600  # seconds after which the statusline's last write is called out


def at(epoch, fmt):
    return datetime.datetime.fromtimestamp(epoch).astimezone().strftime(fmt)


parts = [datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z")]
try:
    usage = json.loads(USAGE.read_text(encoding="utf-8"))
    for key, label, fmt in (("five_hour", "5h", "%H:%M"), ("seven_day", "7d", "%a %H:%M")):
        limit = usage["rate_limits"].get(key)
        if limit:
            parts.append(f"{label} {limit['used_percentage']:.0f}% (resets {at(limit['resets_at'], fmt)})")
    age = time.time() - usage["written_at"]
    if age > STALE:
        parts.append(f"usage last read {age / 60:.0f} min ago")
except (OSError, ValueError, KeyError, TypeError):
    parts.append("usage unknown (no statusline data; /dory:init sets it up)")
print("[dory] " + " · ".join(parts))
