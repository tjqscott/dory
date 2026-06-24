<p align="center">
  <img src="images/dory.png" alt="Dory" height="300">
</p>

<h1 align="center">Dory</h1>

<p align="center">
  <em>Stateless context management for LLM sessions.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/tjqscott/dory?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/badge/release-v2.0.0-111111?style=flat-square" alt="Release 2.0.0">
  <img src="https://img.shields.io/badge/works%20with-Claude%20%7C%20ChatGPT%20%7C%20Local-111111?style=flat-square" alt="Works with Claude, ChatGPT, Local LLMs">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

---

---

Long, continuous chat threads drain token quotas, dilute context, and tie your project state to ephemeral browser instances.

Dory treats hosted LLM interfaces as disposable tools. By offloading state to your local environment and enforcing atomic sessions, you maintain a low baseline token usage and secure your codebase history.

---

### 🧠 Strategy

| Traditional Sessions | Dory Atomic Sessions |
| --- | --- |
| **Bloated:** History re-parsed every turn. | **Lean:** Only active task state loaded. |
| **Volatile:** Chat deletion drops state. | **Persistent:** History saved to local vault. |
| **Expensive:** Context limits hit fast. | **Efficient:** Baseline token usage constant. |

---

### 📂 Repository Structure

Dory integrates directly into your project's version control.

```text
your-project-root/
├── .dory/
│   ├── agents.md             # Operational directives and behavior
│   └── history/              # Local vault for session summaries and code
├── CHANGELOG.md              # Architectural decision ledger

```

---

### 🛠️ Implementation Options

Dory operates as either a manual prompt framework or an automated CLI skill.

* **Pure Prompt (Web UI):** Pass the contents of `.dory/agents.md` and `CHANGELOG.md` in your initial message to establish operational boundaries.
* **CLI Skill:** Configure `.clauderc` (or an equivalent tool configuration) to automatically inject these directives into the system prompt for local agents.

---

### ⚙️ Operational Directives (`agents.md`)

Dory relies on configuration to maintain execution speed and precision.

#### I. Core Behaviors

* **Intent-First:** The model prioritizes structural goals over literal text.
* **Zero-Padding:** No conversational wrapping. Output code blocks directly.
* **Decomposition:** Explicit `[PLANNING]` ➔ `[IMPLEMENTING]` ➔ `[TESTING]` flow for complex tasks. This is optional for small or isolated requests.

#### II. Tactical Engineering

* **Minimalism:** Clean, flat code. No defensive boilerplate or redundant abstractions.
* **Terminal Aesthetics:** Structured formatting for clean and real-time output feedback.
* **Verification:** Probes the directory and verifies state before acting. Avoids assumptions.

#### III. Vault Protocols

* **Append-Only Ledger:** High-density, single-line decision tracking.
* **Artifact Vaulting:** Sessions conclude with a `.md` summary and clean code snippets saved locally.
* **Token Gating:** Every response includes a token metric to signal context saturation.

---

### 🚀 Workflow Cycle

1. **Initialize:** Open a fresh chat. Load `CHANGELOG.md` and `.dory/agents.md`.
2. **Probe:** The model inspects the local environment.
3. **Execute:** The model delivers direct code.
4. **Monitor:** Track the token metrics to manage quota limits.
5. **Persist and Clear:** Save the summary to the vault, append the decision to the log, and terminate the session.

*He says nothing. He writes one line. It works.*
