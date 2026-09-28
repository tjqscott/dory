---
name: handoff
description: Write one self-contained goal that a fresh session can continue from. Use when context is running out, before clearing a session, when usage passes 95% on a long run, or when asked for a handoff.
---

# Handoff

1. **Write one entry at the top of `## Now`** in `wiki/tickets.md`, containing:
   - the goal, and the check that proves it done;
   - the current state: branch, last commit, anything running and where its output lands;
   - the files to read first;
   - what was ruled out, naming the `tried.md` rows in backticks.
2. **It must stand alone.** A fresh session holding only AGENTS.md, `wiki/index.md` and this entry can continue without asking what happened.
3. **Print the entry** so the user can paste it too.
