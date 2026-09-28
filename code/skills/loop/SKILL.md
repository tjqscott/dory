---
name: loop
description: Work through the taskboard unattended for hours, pacing against the usage limits and filling the gap before a reset with CPU-only jobs. Use when asked to run all day, work unattended, or loop over tickets.
---

# Loop

Follow AGENTS.md VI. Every prompt carries a `[dory]` line with the time and the five-hour usage.

1. **Pick** the top item under `## Now` in `wiki/tickets.md`, or else `## Next`. State its check before starting.
2. **Work it.** When its check passes, run the learn skill on what it taught and move it to `## Done`.
3. **Before each new item, read the `[dory]` line:**
   - **Below 90%:** continue.
   - **90% or more:** start no model-heavy item. Finish the current one, and queue jobs that need no model under `## CPU`, each with its command and output path.
   - **95% or more:** launch every `## CPU` job in the background with its output going to a file, run the handoff skill, and start nothing else.
   - **At 100%**, Claude Code pauses and resumes after the reset (wait and continue, v2.1.234+). On resume, read the handoff first, collect the CPU outputs, and carry on from step 1.
4. **If usage is unknown** (no statusline data), say so once and pace by the clock instead.
5. **Never** push, merge or delete unless the project's own instructions already allow it.
