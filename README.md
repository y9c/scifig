# scifig

Publication figures with plain matplotlib. No package.

## Use it (already cloned)

The repo is <your path>/scifig. Point the agent at it, or run it in this folder. The agent should only **read** `skill/` + `examples/` and make your figure — it does **not** clone anything.

```bash
make venv                        # .venv with matplotlib/numpy/scipy (once)
cd examples && ../.venv/bin/python grouped_bar.py   # -> out/grouped_bar.pdf
```

If that PDF renders, the env works. Then read `skill/SKILL.md` and make the figure.

## If it's not cloned yet

`git clone https://github.com/y9c/scifig.git && cd scifig` — do this once yourself, **not** by the agent.
