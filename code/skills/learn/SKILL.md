---
name: learn
description: Record a correction, decision, finding or failed attempt in the wiki. Use when the user corrects you, when a decision is made with a reason, when an experiment returns a verdict, or when you learn something the next session would otherwise re-derive.
---

# Learn

1. **Filter.** Keep it only if it will matter in the next 10 sessions and a stranger could act on it without this session. Otherwise drop it and say so in one line.
2. **Find the owner.** Read `wiki/index.md`. A decision is a row in `decisions.md`. A hypothesis and its verdict is a row in `tried.md`. Anything else goes on the page whose subject it is.
3. **Edit in place.** Replace the sentence or row it contradicts, keeping one line on what overturned the old claim. Create a new page only when no page owns the subject, and link it from its parent in the same edit. Follow AGENTS.md III and V.
4. **Lint** with `python <plugin>/code/scripts/wiki_tree.py wiki` (the plugin root is two levels above this skill's base directory). It must report 0 problems.
5. **Report** the change in one line.
