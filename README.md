# scifig

**Publication-grade scientific figures with matplotlib** — a thin, agent-first
harness. Describe the figure (declarative or object-oriented); scifig applies the
house style, semantic colors, polish, and vector export for you.

## Install

```bash
make setup     # reproducible: .venv + package (uv, Python 3.11)
make figs      # regenerate all example figures (vector PDFs)
```

Or plain: `pip install -e .` (add `[mcp]` for the MCP server, `[examples]` for scipy).
`uv.lock` is committed so every machine builds the same environment.

**For an agent (or yourself) doing a fresh setup, give it
[`docs/install-prompt.md`](docs/install-prompt.md)** — the copy-paste uv
setup + smoke-test procedure.

## Quick start

```python
import matplotlib; matplotlib.use("Agg")
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.0))
fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("single"))
scifig.make_grouped_bar(ax, ["A", "B"], [[0.9, 0.8], [0.7, 0.6]], ["Ours", "Base"],
                        ylabel="Score")
scifig.finalize_figure(fig, "out/fig")   # -> out/fig.pdf (vector)
```

## Three ways to build a figure

| Way | Use | Example |
|-----|-----|---------|
| **Declarative** | most figures | `scifig.FigureSpec(panels=[...])` + `render_spec` |
| **Object-oriented** | typed panels | `scifig.Figure()` + `add(BarPanel(...))` |
| **Archetype** | one common shape, one call | `scifig.timeseries_ci(...)`, `scifig.sorted_bar(...)` |

## Bioinformatics (recipes, not package features)

Domain figures are **examples** in `examples/`, built from scifig primitives —
the agent reads and adapts them. Two shared recipe modules:

* `examples/biofigs.py` — `volcano`, `ma_plot`, `dot_plot`, `umap_scatter`,
  `violin_groups`
* `examples/proteinfig.py` — `pymol_cartoon` (PyMOL, publication PNG) and
  `matplotlib_cartoon` (vector PDF/SVG via real PDB coordinates + SSE)

See `docs/protein-rendering.md`: PyMOL output is **raster**; for a true vector
cartoon use the matplotlib recipe (or cellscape / FlatProt SVG).

```python
from proteinfig import pymol_cartoon
pymol_cartoon("5JJ4", "out/aicda.png", chain="A")   # needs brew install pymol
```

Runnable demos in `examples/diff_exp`, `examples/single_cell`, `examples/rna_seq`.

## Conventions baked in

Nature-style Arial ~5-6pt at final column width; semantic colors (blue=ours,
green=improvement, red=baseline); thin spines, no grid clutter; editable vector
text (`pdf.fonttype=42`); exact-size save (`savefig.bbox=standard`); auto layout
audit (no panel overlap); panel letters at the corner.

See `docs/architecture.md` (skill / MCP / engine), `AGENT.md`, and `skill/`.