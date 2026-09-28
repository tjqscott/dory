---
name: init
description: Set up Dory in this repo by exploring it, creating wiki/ from the template, and connecting the usage statusline. Use when a project has no wiki/ yet, or when asked to set up Dory.
---

# Set up Dory

Paths are relative to this skill's base directory. Run scripts with Python 3.

1. **Explore before writing.** Read the README and any docs. Run a tree of the repo to depth 3, skipping dependency and build folders, and `head` a few data files. Note anything that already records decisions or findings (a CHANGELOG, `docs/`, a findings file).
2. **Create `wiki/`** by copying `../../wiki-template/` into the repo root. Never overwrite a file that exists.
3. **Fill the index.** Add a line to `wiki/index.md` for each real module or subject found in step 1, saying when to open it. Create a page only for something a stranger could not get from the code (AGENTS.md V, What Earns a Page). Copy existing decisions and findings into `decisions.md` and `tried.md`, and tell the user which originals are now superseded; don't delete them.
4. **Lint:** `python ../../scripts/wiki_tree.py wiki --write` from the repo root. It must report 0 problems.
5. **Usage statusline.** Ask before changing settings. Hooks can't see rate limits, so the prompt hook's usage numbers come from the statusline. If the user agrees, set `statusLine` in `~/.claude/settings.json` to a command running `sh <plugin>/code/hooks/py.sh <plugin>/code/scripts/usage_statusline.py`, with real absolute paths. If a statusline exists already, show the user what to add to it instead of replacing it.
6. **Obsidian (optional).** Offer to link `wiki/` into the user's vault so it shows in their graph. On Windows, `mklink /J "<vault>\<project>" "<repo>\wiki"` works without admin. Elsewhere, `ln -s "<repo>/wiki" "<vault>/<project>"`.
7. **Report** what was created and the lint result.
