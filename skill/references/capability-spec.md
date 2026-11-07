# scifig Capability Spec (agent-facing)

scifig is **pure skill** — no Python package, no environment to install. It is a
set of standards + reference recipes. The agent reads this and the examples,
then implements any figure **in the user's own environment with plain
matplotlib**. scifig guarantees the *look* (via the copy-paste house style); the
agent supplies the *figure logic*.

## What scifig provides

| Concern | Where |
|---------|-------|
| Look & conventions (copy-paste) | [house-style.md](house-style.md) — rcParams + helpers + palette |
| Capability map (this file) | what figure types are covered and how |
| Working recipes | [../examples/](../../examples/) — runnable with plain matplotlib |
| Agent workflow | [figure-guidelines.md](figure-guidelines.md) — ask-first, polish, verify |

**There is nothing to install.** Paste the house-style preamble, write the plot,
save a vector PDF. Done.

## Universal rules (every figure)

- Arial ~5-6pt at final column width; lowercase Nature letters / uppercase bold Science.
- Semantic colors (blue=key, green=improve, red=baseline); never hardcode hex.
- Thin spines, subtle-or-off grid, readable/minor ticks, panel letters at corner.
- Units + N + uncertainty on the figure.
- Vector-first: PDF primary; `pdf.fonttype=42`; `savefig.bbox=standard`.
- Reproducible: read data from a path; no inline data > ~20 rows.
- **Verify before claiming done**: re-open the saved figure and confirm no overlap,
  no clipping, letters clear, legend placed.

## Figure types covered (the capability map)

Each row: a figure type, and the reference recipe it's built from. **All are
recipes** — the agent reads the example and re-implements in the user's env.

| Figure type | Reference example |
|-------------|-------------------|
| Grouped / single bars (+ error bars) | `examples/grouped_bar.py`, `benchmark_parity.py` |
| Trend / curves + confidence band | `examples/trends_grid.py` |
| Heatmap + colorbar | `examples/heatmap.py` |
| Scatter | `examples/compose_annotate.py` |
| Multi-panel grid + shared legend | `examples/benchmark_nature.py` |
| Quantitative comparison (bars + error + right legend) | `examples/benchmark_parity.py` |
| Volcano / MA (differential expression) | `examples/biofigs.py`, `examples/single_cell/` |
| Marker dot plot / UMAP / violin (single-cell) | `examples/biofigs.py` |
| RNA-seq QC bars | `examples/rna_seq/` |
| Protein cartoon (PyMOL, raster) | `examples/proteinfig.py` |
| Protein topology (matplotlib, vector) | `examples/proteinfig.py`, `showcase_protein.py` |
| Inset / composition | `examples/showcase_inset.py` |

> Protein vector-vs-raster: see [protein-rendering.md](protein-rendering.md).

> The agent picks the closest example, reads it, and implements the figure in
> the user's environment. **It does not install or depend on a scifig package.**

## The universal pattern

Every figure follows the same shape — this is the contract that keeps output
consistent.

```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# 1) style (paste the house-style preamble)
plt.rcParams.update({...})          # see house-style.md
# 2) figure at final physical size
fig, ax = plt.subplots(figsize=nature_figsize("single"))
# 3) any plot logic
# 4) polish (readable ticks, subtle grid, panel letter)
# 5) vector-first save
save(fig, "out/fig")              # -> out/fig.pdf
```

## Agent workflow (ask first, then implement)

1. **Ask up to 5 questions** (claim / venue+width / panels / data / chart type).
2. **Pick the closest example** from the capability map; read it.
3. **Apply the house style** (paste the preamble) + universal rules.
4. Implement the figure in the user's env with plain matplotlib.
5. **Verify**: re-open the saved figure, confirm no overlap/clipping, letters
   clear, legend placed. Only then claim done.

## Extending (new figure types)

Add a **new example** under `examples/` (a plain-matplotlib script following the
house style), and a row in this table. No package to grow — the skill stays lean.
