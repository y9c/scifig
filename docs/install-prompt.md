# Agent install prompt — set up scifig with uv

Give this to an agent (or paste it as your first instruction) to install and
verify the scifig plotting environment. It is a complete, self-contained
setup-and-smoke-test procedure.

---

## Prompt (copy/paste to the agent)

> You are setting up the **scifig** publication-figure environment and verifying
> it works. Follow these steps exactly, in order. scifig is managed entirely by
> **uv** (one lockfile, reproducible across machines).
>
> **1. Check prerequisites.**
> - `uv` installed? (`uv --version`). If missing: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then reload shell.
> - Python 3.10+ available? (uv will build its own if not.)
>
> **2. Create the environment from the lockfile (no manual dependency decisions).**
> ```bash
> make setup          # = uv venv --python 3.11 .venv && uv pip install -e ".[dev,examples]"
> ```
>
> **3. Verify the install.**
> ```bash
> .venv/bin/python -c "import scifig; print('scifig', scifig.__version__)"
> .venv/bin/python -c "import matplotlib, numpy; print('mpl', matplotlib.__version__)"
> ```
>
> **4. Regenerate the reference figures (proves end-to-end).**
> ```bash
> make figs
> ```
> Every example should write an `out/<name>.pdf` (vector) and `.png` (preview).
> If any fails, report the exact failing script + traceback; do not silently skip.
>
> **5. Optional extras, only if needed.**
> - MCP server: `uv pip install -e ".[mcp]"` (needs Python >=3.10) then `make mcp`.
> - Bio/protein demos already run as part of `examples/` (volcano, UMAP, dot plot,
>   protein cartoon). PyMOL cartoon needs `brew install pymol` on macOS.
>
> **6. Report back.** State: `uv` version, `scifig` version, matplotlib version,
> number of figures generated, and any failure. Do not rename or regenerate
> `uv.lock` unless dependencies changed (then run `make lock`).

---

## Notes for humans

- `make setup` is idempotent; safe to re-run.
- `uv.lock` is committed — never hand-edit it; use `make lock` to refresh after
  changing `pyproject.toml`.
- On a fresh clone this is the whole setup: no per-machine tweaks, no manual
  `pip install` of individual packages.
- If the machine lacks `make`/`uv`, the agent should say so and give the raw
  `uv venv` / `uv pip install` equivalent.
