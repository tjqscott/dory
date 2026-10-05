# Notes benchmark

Can a local model keep project notes? Each trial gives the model the same notes and one changed fact, and asks for the change three ways:

| Method | The model returns |
|---|---|
| `rewrite` | the whole notes file, with one line changed |
| `patch` | a SEARCH/REPLACE block for that line |
| `append` | a Dory post that replaces the old fact |

A trial passes only if the notes end up saying exactly the right things. Markdown decoration (bold markers, bullet dashes) may differ; a missing fact, a changed fact or a dropped reason fails. Each method gets one retry with the error it would see in real use. Notes come in three sizes: 20, 60 and 150 facts.

## Results

Run on 4 October 2026: 20 trials per cell, each model's own default temperature, Ollama 0.34.1 on an Apple M5 Max. [`results/run.json`](results/run.json) has the hardware, model digests and limits.

<!-- gen: notes_bench.py — 2026-10-05 -->
| Model | Facts | Method | First try | After one retry | Tokens out |
|---|---|---|---|---|---|
| gemma4:12b-it-qat | 20 | rewrite | 95% | 95% | 888 |
| gemma4:12b-it-qat | 20 | patch | 55% | 80% | 1,934 |
| gemma4:12b-it-qat | 20 | append | 90% | 95% | 1,170 |
| gemma4:12b-it-qat | 60 | rewrite | 100% | 100% | 1,462 |
| gemma4:12b-it-qat | 60 | patch | 85% | 100% | 2,880 |
| gemma4:12b-it-qat | 60 | append | 95% | 95% | 1,052 |
| gemma4:12b-it-qat | 150 | rewrite | 100% | 100% | 2,530 |
| gemma4:12b-it-qat | 150 | patch | 100% | 100% | 3,258 |
| gemma4:12b-it-qat | 150 | append | 100% | 100% | 1,059 |
| qwen3:8b | 20 | rewrite | 65% | 75% | 846 |
| qwen3:8b | 20 | patch | 25% | 35% | 1,297 |
| qwen3:8b | 20 | append | 90% | 90% | 660 |
| qwen3:8b | 60 | rewrite | 45% | 50% | 1,625 |
| qwen3:8b | 60 | patch | 25% | 25% | 1,578 |
| qwen3:8b | 60 | append | 70% | 70% | 774 |
| qwen3:8b | 150 | rewrite | 30% | 35% | 2,556 |
| qwen3:8b | 150 | patch | 0% | 0% | 1,871 |
| qwen3:8b | 150 | append | 85% | 85% | 630 |
<!-- /gen -->

**Gemma 4 12B passed 173 of 180 trials, and all 60 at 150 facts.** Qwen3 8B passed 93 of 180: it could append (49 of 60) but not rewrite (32 of 60) or patch (12 of 60).

Limits of this run:

- 20 trials per cell is small. A single cell can move by 20 points between runs.
- The notes are synthetic, and the same line can appear in several sections, which makes `patch` harder than on most real files.
- 29 requests ran out of generation budget while the model was still thinking, mostly Gemma's 20-fact patches. Those count as failures.

## Run it

```bash
python3 bench/notes_bench.py --selftest
```

```bash
python3 bench/notes_bench.py --models qwen3:8b gemma4:12b-it-qat
```

It needs Python 3 and a running [Ollama](https://ollama.com); nothing else. Use the model tags `ollama list` shows. Every request and reply is saved to `results/<model>.responses.jsonl`, so the scores can be rebuilt with no model:

```bash
python3 bench/notes_bench.py --rescore
```
