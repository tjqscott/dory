# Notes benchmark

Can a local model keep project notes? Each trial gives the model the same notes and one changed fact, and asks for the change three ways:

| Arm | The model returns |
|---|---|
| `rewrite` | the whole notes file, with one line changed |
| `patch` | a SEARCH/REPLACE block for that line |
| `append` | a Dory post that replaces the old fact |

A trial passes only if the notes end up exactly right. Each arm gets one retry with the error it would see in real use. Notes come in three sizes: 20, 60 and 150 facts.

```bash
python3 bench/notes_bench.py --selftest
```

```bash
python3 bench/notes_bench.py --models qwen3:8b
```

It needs Python 3 and a running [Ollama](https://ollama.com); nothing else. Use the model tags `ollama list` shows. Results and `chart.svg` land in `bench/results/`.
