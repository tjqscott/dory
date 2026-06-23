<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/banner.png">
    <img src="images/banner.png" width="220" alt="Dory, the stateless memory manager">
  </picture>
</p>

<h1 align="center">Dory</h1>

<p align="center">
  <em>Every new chat starts blind. Burn through the context, not your quota.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/taylorscott/dory?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <strong>Predictable Token Burn &middot; Stateless Interactions &middot; 100% Local Portability &middot; Zero Data Loss</strong><br>
  <sub>Designed for strict cost-defense in standard Claude Pro web sessions. By moving from continuous chat transcripts to atomic execution and local history extraction, you eliminate exponential context re-parsing overhead entirely.</sub>
</p>

---

You know the routine. You burn through a context window, switch models, or just close a tab and come back tomorrow. Now you're spending the first ten messages re-explaining your project to an AI that has no idea what you built yesterday.

Dory resolves context bloat, data loss, and platform dependencies by treating hosted LLM sessions as completely volatile, disposable scratchpads. By maintaining a lean, local architectural ledger alongside a deconstructed artifact vault, you can hard-reset chat sessions continuously—minimizing token consumption and protecting your code history.

## Before / after

*   **Before:** A massive, single chat thread spanning hours. Every message scales quadratically in token cost as Claude re-parses the entire history, rapidly triggering your tier rate limits and degrading response accuracy. One accidental click deletes the tab, wiping out critical code variations.
*   **After:** Atomic execution. You open a fresh tab, feed it the lean single-line ledger, execute a single scoped task, and export a clean markdown post-mortem to your local vault. The chat is safely deleted immediately after completion, keeping your token baseline at zero.

---

## Repository Structure

```text
your-project-root/
├── .dory/
│   ├── agents.md             # Global directives, behavioral rules, and tactical engineering rules
│   └── history/              # Vault for mid-sized chat summaries and historic code snippets
│       ├── 20260624_auth.md  # Session post-mortem (mandatory)
│       └── 20260624_auth.py  # 0 to N raw code snapshots / reference variations
└── CHANGELOG.md              # Lean, single-line, append-only architectural decision ledger
