# Dory Directives

How an agent works on a project that uses Dory. Sections I–III apply everywhere. Section IV applies in a browser chat, where `dory.html` supplies the posting format. Sections V and VI apply where the agent can read and write the repo (Claude Code, Codex).

## I. Core Behaviors
* **Intent-First:** Prioritize structural goals and system architecture over the literal wording of a request. State your assumptions. When a request has more than one reading, name them rather than picking one silently. When something is unclear, stop and ask.
* **Zero-Padding:** No conversational wrapping, introductions or recaps. Lead with the answer or the code.
* **Decomposition:** For complex tasks, state the phase: `[PLANNING]` ➔ `[IMPLEMENTING]` ➔ `[TESTING]` ➔ `[ITERATING]`. Give each planned step a check that proves it done: "add validation" becomes "a test with invalid input fails, then passes". Optional for small, isolated requests.
* **Diverge, then converge, on visuals:** Offer a few mockups that differ in direction, not in detail. Once one is chosen, refine that one. Build them with real content, end with your pick and why, and treat any reference as inspiration, not a template.

## II. Tactical Engineering
* **Minimalism:** The least code that solves the problem. No speculative features, single-use abstractions, unrequested configuration, handling for impossible errors, or obvious comments. If 200 lines could be 50, rewrite it.
* **Surgical Changes:** Touch only what the request needs, in the style already there. Anything beyond that is named in one line, not done silently. Remove what your own change left unused; mention pre-existing dead code rather than deleting it.
* **Terminal Aesthetics:** Format outputs for clean real-time feedback. Use left/right justification (`.ljust()`), self-flushing prints (`flush=True`), and single-line progress indicators to avoid verbose log clutter.
* **Verification Loop:** Check directory structures and data files before writing code: run `ls`, `grep` and `head` where you can, and ask for their output where you cannot. Do not make assumptions regarding the local environment.
* **Iteration Limits:** If `[TESTING]` fails, enter `[ITERATING]` with the exact error. If iteration stops making progress, record the failing state and recommend a fresh session.

## III. Writing
Anything written to keep (posts, wiki pages, commit messages) follows these rules.
* **Clean:** No conversational framing, no restating the request, no announcing that you are writing.
* **Dense:** Name the file, the function, the number. "Improved performance" is not a record; "cut `loader.py` N+1, p99 340 ms to 90 ms" is.
* **Human:** Reader-shaped, not session-shaped: organised by subject, not by the order things happened. Say why; git already says what.
* **Stranger Test:** Before writing, ask whether a stranger could act on it without the session it came from. If not, rewrite it or drop it.

## IV. Browser Chat
* **Posts:** End the session by emitting what is worth keeping as posts, in the format the context gives. Never edit an old post; supersede it with `replaces`.
* **Decisions and Tried:** A decision and its reason goes on the `decisions` page. An attempt that failed, and why, goes on the `tried` page. A later verdict replaces the earlier post.
* **No Filesystem:** You cannot run commands or save files. Ask for the output you need, and hand back code with its `path`.

## V. Repo Wiki
The project's memory is `wiki/`: a tree of small pages under `wiki/index.md`.
* **One Parent:** Every page is linked from exactly one parent, and that link is its address. `index.md` is the root.
* **Links Point Down:** A page links its children and its parent, nothing else. When two siblings relate, write the relation into their parent. Refer across the tree in backticks. Links under a `## Related` heading are allowed only inside a finished subtree that its hub declares frozen.
* **What Earns a Page:** Something that would otherwise be re-derived at cost: a schema, a finding that changed the approach, a command easy to get wrong, a decision and its reason. Status, single facts and to-dos are a line in a parent. What the code or git already says earns nothing.
* **Edit in Place:** New information replaces the sentence it contradicts, and a replaced claim keeps one line saying what killed it. Never rewrite a line a human wrote without saying so. No dated or session-shaped pages.
* **Staleness by Tier:** Derived facts (trees, schemas, counts) live inside `<!-- gen: <script> — <date> -->` fences and are regenerated, never hand-edited. Volatile facts (hosts, versions, open problems) carry their date. Settled facts change only when falsified.
* **Budgets:** Hub under 250 words, reference under 400, subject page under 900. Over budget means split along a seam.
* **Findings Ledger:** `wiki/tried.md` holds one row per hypothesis with its verdict and evidence. A new verdict replaces the row and keeps one line on what it overturned. Read it before proposing an experiment.
* **Taskboard:** `wiki/tickets.md` holds the work under `## Now`, `## Next`, `## CPU` (jobs that need no model) and `## Done`. A carried-out plan is folded into the page it changed, then deleted.
* **Lint Before Finishing:** Run the wiki lint. Orphans, unreachable pages, pages with two parents and sideways links must all read zero.
* **History Is an Archive:** Raw session transcripts in `history/` are a safety net, not context. Read one only when pointed at it.

## VI. Long Runs
Each prompt carries a `[dory]` line with the time and the usage of the five-hour limit.
* **Below 90%:** Work from `## Now` on the taskboard.
* **At 90%:** Start no new model-heavy task. Finish the current one, and move jobs that need no model (tests, builds, backtests, scrapes, lint) into `## CPU`.
* **At 95%:** Launch the `## CPU` jobs in the background with their output going to files, and add a handoff line to `## Now`: what is running, where its output lands, what to do with it.
* **At 100%:** The session pauses until the limit resets. On resume, read the handoff before anything else.
