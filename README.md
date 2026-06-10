# Dory 🐟

*An append-only changelog convention that gives your AI the memory it doesn't have.*

---

Every new chat starts blind. You burned through a context window, switched models, or just closed a tab and came back tomorrow. Now you're spending the first ten messages re-explaining your project to an AI that has no idea what you built yesterday.

Dory fixes that with one file.

---

## How it works

Drop a `CHANGELOG.md` in your repo root. Next time you start a chat, include the file in context. The model reads it and picks up where you left off.

That's it.

```markdown
# Project Changelog
<!-- Append-only. One line per entry. No headings or blank lines. -->

Refactored auth to JWT after session logic started breaking under multi-tenant load
Scaffolded the database schema
Fixed a rendering bug in the tree component
```

No structured format to memorise. No tooling to install. Works with any model, any editor, any project.

---

## The file

```markdown
# Project Changelog
<!-- Append-only. One line per entry. No headings or blank lines. -->
```

Copy this header into a file called `CHANGELOG.md` at your repo root and start writing. Git tracks it automatically alongside your code.

Bold and inline code are fine.

---

## Using it with an AI

Drop `CHANGELOG.md` into the context window at the start of a session. To write, tell the model to update the changelog. Most models understand the file on sight, but if you want consistent behaviour across sessions a short system prompt helps:

> Update the changelog. No headings, no blank lines.

---

## Examples

### Automation project

```markdown
# Project Changelog
<!-- Append-only. One line per entry. No headings or blank lines. -->

Architecture settled — single `run.py` with five sequential phases; `state.json` as sole persistence layer
Scan filters added — head-to-head regex, slug blacklist, volume floor, no settled markets
Crash recovery implemented — marks pending entries as placed if already held on sync
Settlement detection via price thresholds; wins trigger FOK sell, losses marked without sell attempt
Fix: in-progress entries bypassed entry window check due to clamped timestamp; explicit guard added
Fix: double-entry guard missed matches when name parsing hit abbreviations; switched to slug-based key
Stake reduced from 5% to 3% after ruin analysis on shuffled historical outcomes
Fix: phantom cashouts — FOK sell success now validated before booking P&L
```

### Visualisation tool

```markdown
# Project Changelog
<!-- Append-only. One line per entry. No headings or blank lines. -->

Initial JS/HTML prototype; Dubins-Spanier ported from Python
Selfridge-Conway and Even-Paz implemented; `common.js` extracted for shared functions
Cut-and-choose added; chart initialisation bug fixed that caused incorrect render on first load
Selfridge-Conway visualisation completed — stack trace, contiguous backgrounds, agent spacing tested to 12
Playback controls added — play/pause and stop-at-end
Dubins-Spanier reimplemented in JS with sliding knife animation and normalised layouts
Polish pass — hover, label consistency, PDF title, doc links
```

### Research project

```markdown
# Project Changelog
<!-- Append-only. One line per entry. No headings or blank lines. -->

Initial structure — search parameters, citations, column selection rationale, language guide with bias classifications
Systematic review writeup begun; pre-search process and extraction methodology documented
experiment-data.csv v1 uploaded; v1.0.1 issued immediately to fix Molokken deduplication
SQL revised to output resolution time instead of effort; filtering criteria clarified
README restructured — repository layout overhauled, completion times corrected to proper units
```

---

## Why not just use git history?

Git history tracks code. Dory tracks decisions. A commit message tells you what changed; a changelog entry tells you why you went in that direction and what state you left things in. They work well together.

If your project already has a `CHANGELOG.md` tracking user-facing releases, name this one `AI_CONTEXT.md` or `LLMLOG.md` instead.

---

## Contributing

This is a convention, not a codebase. If you have a better header, a useful example, or want to add a CLI wrapper, open a PR.

---

## License

MIT
