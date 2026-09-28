#!/bin/sh
# Run a Dory script with whichever Python 3 this machine has. The check runs
# python3 rather than looking it up, because Windows can ship a python3 stub
# that only opens the Store.
if python3 -c "" >/dev/null 2>&1; then exec python3 "$@"; fi
exec python "$@"
