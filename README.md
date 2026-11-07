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
| **Archetype** | one shape, one call | `scifig.volcano(...)`, `scifig.timeseries_ci(...)` |

## Bioinformatics

Domain helpers: `volcano`, `ma_plot`, `dot_plot`, `umap_scatter`, `violin_groups`,
and pure-matplotlib protein topology (`draw_topology`). Runnable demos in
`bio/diff_exp`, `bio/single_cell`, `bio/rna_seq` (each with `data.py` + `plot_*.py`).

## Conventions baked in

Nature-style Arial ~5-6pt at final column width; semantic colors (blue=ours,
green=improvement, red=baseline); thin spines, no grid clutter; editable vector
text (`pdf.fonttype=42`); exact-size save (`savefig.bbox=standard`); auto layout
audit (no panel overlap); panel letters at the corner.

See `docs/architecture.md` (skill / MCP / engine), `AGENT.md`, and `skill/`.