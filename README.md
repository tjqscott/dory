# 🐟 Dory

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

For a model switch or a fresh session after a long gap:

> Read the changelog and tell me where we are.

If you're using Claude, copy `SKILL.md` into your project instructions to set the behaviour once for all sessions.

---

## Examples

See the [`examples/`](examples/) directory for real-world changelogs across different project types.

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
