<p align="center">
  <img src="images/dory.png" alt="Dory" height="300">
</p>

<h1 align="center">Dory</h1>

<p align="center">
  <em>Stateless context management for LLM sessions.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/tjqscott/dory?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/badge/release-v3.0.0-111111?style=flat-square" alt="Release 3.0.0">
  <img src="https://img.shields.io/badge/works%20with-Claude%20%7C%20ChatGPT%20%7C%20Codex%20%7C%20Local-111111?style=flat-square" alt="Works with Claude, ChatGPT, Codex, Local LLMs">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

---

Every new chat starts blind. Long threads drain quotas and dilute context, and closing the tab loses the project. Dory keeps the memory outside the chat, so every session can start fresh and still know what was decided, what was tried, and why.

It comes in two editions, one for each way you work with a model.

| | 🌐 Browser edition | 💻 Code edition |
| --- | --- | --- |
| **For** | any hosted chat: Claude, ChatGPT, Gemini, local models | Claude Code (plugin) and Codex (`AGENTS.md`) |
| **Memory** | posts the model writes, kept in one file you own | a `wiki/` of small linked pages in your repo |
| **Install** | download one HTML file | `/plugin install dory@dory` |
| **Enforced by** | the page, which rejects malformed posts | hooks, which lint the wiki before a session can finish |

---

### 🌐 Browser edition

1. Open [`browser/single-file/dory.html`](browser/single-file/dory.html) in your browser.
2. Click **Copy context** and paste it into a fresh chat. It holds the directives, the posting format, the pages you tick and, if you read it, your project folder's tree and data previews. The size is measured, not guessed.
3. Work. At the end, the model emits posts.
4. Paste its whole reply back, click **Add posts**, then **Save**.

Posts are append-only. A later post supersedes earlier ones with `replaces: 4` or `replaces: all`, so a small model can add notes and a strong one can rewrite a page, and nothing written is lost. The page makes no network calls.

Two stores are under test. [`browser/markdown-store/`](browser/markdown-store/) keeps the posts in a `DORY.md` that renders on GitHub instead. [docs/v3.md](docs/v3.md) has the comparison.

### 💻 Code edition

```text
/plugin marketplace add tjqscott/dory
/plugin install dory@dory
/dory:init
```

| Piece | What it does |
| --- | --- |
| `wiki/` | a strict tree under `index.md`: one parent per page, links point down, derived facts regenerated inside fences |
| `wiki/tried.md` | the findings ledger: every hypothesis and its verdict, so nothing gets run twice |
| `wiki/tickets.md` | the taskboard: Now, Next, CPU, Done |
| Hooks | load the directives and wiki index at start, stamp each prompt with the time and usage, and lint the wiki before stopping |
| Skills | `/dory:init`, `/dory:learn`, `/dory:wrap-up`, `/dory:handoff`, `/dory:loop` |

**Long runs.** `/dory:loop` works the taskboard for hours. At 90% of the five-hour limit it stops starting model-heavy work. At 95% it launches the CPU-only jobs (tests, builds, backtests) and writes a handoff. When the limit resets, it picks up their results.

**Codex.** Codex reads `AGENTS.md`, so copy it into your project root. The skills use the `SKILL.md` format.

**Obsidian.** Link `wiki/` into your vault to see every project's wiki in one graph. On Windows, `mklink /J` needs no admin. [Graph Spawn](https://github.com/tjqscott/obsidian-graph-spawn) keeps each project as its own cluster. Install it from Obsidian's Community plugins.

---

### ⚙️ Directives ([`AGENTS.md`](AGENTS.md))

| Section | Applies to | In short |
| --- | --- | --- |
| I. Core Behaviors | all | intent first, no padding, phases with checks, diverge then converge on visuals |
| II. Tactical Engineering | all | minimal and surgical code, clean terminal output, look before writing |
| III. Writing | all | clean, dense and human, and a stranger could act on it |
| IV. Browser Chat | browser | posts, `replaces`, the `decisions` and `tried` pages |
| V. Repo Wiki | code | tree rules, findings ledger, taskboard, lint |
| VI. Long Runs | code | usage thresholds, CPU jobs across the reset, handoff |

*He says nothing. He writes one line. It works.*

---

### ⭐ Star History

<a href="https://www.star-history.com/#tjqscott/dory&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=tjqscott/dory&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=tjqscott/dory&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=tjqscott/dory&type=Date" />
 </picture>
</a>
