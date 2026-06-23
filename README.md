# Dory 🐟

Every new chat starts blind. You burn through a context window, switch models, or close a tab, and find yourself spending the first ten messages re-explaining your project state. 

Dory resolves context bloat, data loss, and platform dependencies by treating hosted LLM sessions as completely volatile, disposable scratchpads. By maintaining a lean, local architectural ledger alongside a deconstructed artifact vault, you can hard-reset chat sessions continuously—minimizing token consumption and protecting your code history.

## System Components

### 1. The Global Directive Layer (`.dory/agents.md`)
This file establishes the operational boundaries for the LLM. It forces task decomposition, enforces minimalist code output, and mandates token usage reporting. Copy these directives into your global system prompt or reference them at the start of a session.

### 2. The Micro-Context Bridge (`CHANGELOG.md`)
A strict, append-only ledger tracking core architectural decisions. It serves as the primary context injector when initializing a blank chat tab.

### 3. The Artifact Vault (`.dory/history/`)
Isolates complex logic blocks and mid-sized session post-mortems so they are preserved locally when a chat thread is deleted.

---

## Configuration Protocol

Drop the following blocks directly into your project configuration or initialization prompts.

### Core Behavioral Directives
*   Prioritize long-term structural intent over shallow literal interpretation of prompts.
*   Zero conversational wrapping, introductions, or summary padding. Output code blocks immediately.
*   Execute tasks via explicit phased decomposition: [PLANNING/PROBE] ➔ [IMPLEMENTING] ➔ [TESTING].

### Tactical Engineering Rules
*   Code Minimalism: No redundant try-catch blocks, no needless helper abstractions, no obvious comments. Keep logic flat and direct.
*   Terminal Aesthetics: Use left/right justification (`.ljust()`), self-flushing prints (`flush=True`), and single-line progress indicators. Avoid verbose log clutter.
*   Verification Loop: Prioritize terminal probe scripts (`head`, `ls`, `grep`) to check structural reality before writing code. Avoid assumptions.

### Logging, Quota & Vault Protocols
*   Maintain CHANGELOG.md as a single-line, append-only file using the formula: Action + Component + Reason. Moderate length is acceptable for deep architectural rationale. Exclude transient fixes.
*   Post-session, generate a mandatory mid-sized text summary (.md). Pair it with 0 to N raw code snapshots (.ext) tracking notable logic variations.
*   Resource Metrics: Append the absolute cumulative session token estimate and the current turn token weight to the absolute end of every response.

---

## The Workflow Cycle

1. **Initialize:** Open a fresh chat tab. Drop in `CHANGELOG.md` and `.dory/agents.md`.
2. **Probe:** The model executes the `[PLANNING/PROBE]` phase, outputting minimal shell commands to verify directory state or file schemas.
3. **Execute:** The model delivers flat, un-wrapped code. You verify it locally via the provided `[TESTING]` instructions.
4. **Monitor:** Track the absolute token weight reported at the bottom of the responses to watch for context accumulation.
5. **Persist & Clear:** Before the context window bloats, prompt the model to generate the mid-sized `.md` summary and raw code variants for your vault. Append the single-line entry to `CHANGELOG.md`, commit the files to git, and clear or delete the chat thread.
