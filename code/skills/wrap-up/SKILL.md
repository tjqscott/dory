---
name: wrap-up
description: Close out a task by folding what it taught into the wiki, updating the taskboard, and linting. Use at the end of a task, before clearing a session, or when asked to wrap up.
---

# Wrap up

1. **Harvest.** Read this session's human turns first; they hold most of the decisions. Collect every decision and its reason, every correction, and every verdict. Pass each through the learn skill's filter and route it to its owning page.
2. **Taskboard.** In `wiki/tickets.md`, move finished items to `## Done` with one line each (and the commit or PR). Fold a carried-out plan's findings into the pages it changed, then delete the plan.
3. **Lint and refresh** with `python <plugin>/code/scripts/wiki_tree.py wiki --write` (the plugin root is two levels above this skill's base directory). It must report 0 problems.
4. **Report** the pages changed and the tickets moved. "This session produced nothing durable" is a valid result; don't manufacture pages.
