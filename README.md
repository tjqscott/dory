<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/banner.png">
    <img src="images/dory.png" width="333" alt="Dory, the stateless memory manager">
  </picture>
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

Long, continuous LLM sessions result in context degradation, data loss upon session termination, and quadratic token usage scaling. Dory mitigates this by enforcing an atomic session structure. Hosted chat interfaces are treated as volatile scratchpads. State is preserved locally through a compressed architectural ledger and a deconstructed artifact vault, allowing frequent session resets without losing project trajectory.

## State Comparison

* **Continuous Session:** The session history scales exponentially per prompt. Context re-parsing accelerates rate limit depletion and degrades output accuracy over time.
* **Atomic Execution:** A session is initialized with a compressed ledger. A single scoped task is executed. State is extracted locally, and the session is explicitly terminated. The token baseline remains near zero.

---

## Repository Structure

```text
your-project-root/
├── .dory/
│   ├── agents.md             # Global directives, behavioral rules, and engineering constraints
│   └── history/              # Vault for session summaries and raw code iterations
│       ├── 20260624_auth.md  # Session text summary
│       └── 20260624_auth.py  # Associated code snapshots
└── CHANGELOG.md              # Single-line, append-only architectural decision ledger

```

---

## Configuration Protocol & System Decisions

The following directives formulate the `.dory/agents.md` configuration. They establish strict operational boundaries designed to minimize token waste and enforce local state retention.

### Core Behavioral Directives

This section governs task scope and interpretation constraints to prevent unprompted code generation and conversational bloat.

* **Intent Alignment:** Prioritize long-term structural intent over shallow literal interpretation of prompts. *Decision: Prevents the model from writing code that fulfills the immediate request but breaks the broader system architecture.*
* **Zero-Padding Outputs:** Zero conversational wrapping, introductions, or summary padding. Output code blocks immediately. *Decision: Reduces token consumption per turn by eliminating generated prose.*
* **Decomposed Execution:** Execute tasks via explicit phased decomposition: `[PLANNING/PROBE]` ➔ `[IMPLEMENTING]` ➔ `[TESTING]`. *Decision: Forces the model to evaluate the environment and request missing data before attempting an implementation.*

### Tactical Engineering Rules

This section governs code formatting, output aesthetics, and pre-execution verification.

* **Code Minimalism:** No redundant try-catch blocks, no needless helper abstractions, no obvious comments. Keep logic flat and direct. *Decision: Generates lean execution paths that consume less context space in future queries.*
* **Terminal Aesthetics:** Use left/right justification (`.ljust()`), self-flushing prints (`flush=True`), and single-line progress indicators. Avoid verbose log clutter. *Decision: Ensures script execution remains visible without spamming the terminal or logging unnecessary text.*
* **Verification Loop:** Prioritize terminal probe scripts (`head`, `ls`, `grep`) to check structural reality before writing code. Avoid assumptions. *Decision: Eliminates hallucinated file paths and incorrect data schema assumptions.*

### Logging, Quota & Vault Protocols

This section dictates how data is extracted from the ephemeral chat session and stored locally.

* **Ledger Maintenance:** Maintain `CHANGELOG.md` as a single-line, append-only file using the formula: Action + Component + Reason. Exclude transient fixes. *Decision: Creates a high-density, low-token context bridge for initializing new chat sessions.*


* **Artifact Vaulting:** Post-session, generate a mandatory text summary (`.md`) paired with 0 to N raw code snapshots (`.ext`) tracking notable logic variations. *Decision: Preserves complex logic blocks and decision narratives locally, protecting against data loss when a chat tab is closed.*
* **Resource Metrics:** Append the absolute cumulative session token estimate and the current turn token weight to the absolute end of every response. *Decision: Provides manual visibility into context saturation to signal when a session reset is required.*

---

## The Workflow Cycle

1. **Initialize:** Open a fresh chat tab. Supply `CHANGELOG.md` and `.dory/agents.md`.
2. **Probe:** Execute the `[PLANNING/PROBE]` phase. Run the generated shell commands to verify directory state.
3. **Execute:** Implement the flat, un-wrapped code. Verify it locally via the provided `[TESTING]` instructions.
4. **Monitor:** Track the absolute token weight reported at the bottom of the responses.
5. **Persist & Clear:** Generate the summary and code variants for the local vault. Append the single-line entry to `CHANGELOG.md`. Commit the files to version control and terminate the chat session.
