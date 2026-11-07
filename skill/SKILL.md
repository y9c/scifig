---
name: scifig
description: >-
  Publication-grade matplotlib scientific figures (personalized): wraps your two
  preferred styles (scientific_publication / modern), plot-type helpers (grouped
  bars / trend / heatmap / scatter / sphere illustration), and pure-Python
  compose + annotation helpers (panel_grid, join_figures, shared_legend,
  add_panel_label, add_inset, add_bracket/add_sig). Use when making formal
  figures for papers, reports, or slides, or when reusing this repo's house style
  and the scifig package. Do not use for interactive dashboards (Plotly/Altair/
  Bokeh), publication-less EDA-only plots, dominant 3D/GIS workflows, or
  Illustrator/Figma-first infographics. Trigger words: scientific figure,
  publication figure, matplotlib, grouped bar, heatmap, multi-panel, figures4papers.
---

# scifig — Publication-grade scientific figures (matplotlib)

This skill is bound to the `scifig` project (this repo). It is a personalized
integration of: **publication style + modern style + pure-Python compose/annotate**.
Core philosophy: the style lives entirely in the package; your code writes only data.

## When to use

- Making formal **paper / slide / report** figures with matplotlib, needing a
  publication look.
- Involving **grouped bars, trend lines, heatmaps, multi-panel grids, PDF/SVG/high-DPI** output.
- Wanting to **combine several panels in pure Python and annotate them** (panel
  letters, shared legend, inset, significance bracket, stitch saved figures).

## When not to use

- **Plotly / Altair / Bokeh** interactive, web-first.
- **EDA-only** with no publication target (seaborn/pandas suffice).
- Dominant **3D, GIS**, or non-matplotlib workflow.
- **Illustrator / Figma-first** infographics (not matplotlib data plots).

## Quick start

### A: use the scifig package (recommended)

```python
import scifig

# Paper figure: publication style + larger type
scifig.apply_publication_style(scifig.FigureStyle(font_size=18))
fig, ax = scifig.create_subplots(1, 1)
scifig.make_grouped_bar(
    ax, ["A", "B", "C"], [[0.9, 0.8, 0.7], [0.7, 0.6, 0.5]],
    ["Ours", "Baseline"], ylabel="Score", annotate=True,
)
scifig.finalize_figure(fig, "out/fig")   # -> out/fig.pdf (vector-first)
```

Slides/reports: `scifig.apply_modern_style()`.

### B: use only the .mplstyle file

```python
import matplotlib.pyplot as plt
plt.style.use("<repo>/scifig/assets/scientific_publication.mplstyle")
```

## File map

> **Agents start here:** read [references/figure-guidelines.md](references/figure-guidelines.md)
> **first** — it is the agent-first contract: the two mandatory questions, the
> fixed decision ladder, the polish checklist, hard rules, and the code template.

| File / dir | Open when |
|-----------|----------|
| [references/figure-guidelines.md](references/figure-guidelines.md) | **FIRST** — how to build any figure as an agent (contract + template) |
| [references/api.md](references/api.md) | all scifig function signatures, PALETTE, FigureStyle, validation |
| [references/cookbook.md](references/cookbook.md) | **code cheatsheet**: 7 figure types, palette hex, multi-panel/inset/stat annotation, mplstyle reference |
| [references/tutorials.md](references/tutorials.md) | end-to-end flows (bars / trends / heatmap / multi-panel) |
| [references/design-theory.md](references/design-theory.md) | layout, export policy, palette rationale |
| [references/common-patterns.md](references/common-patterns.md) | layout patterns, legend panel, print-safe bars |
| [references/demos.md](references/demos.md) | real top-venue figure script index (this repo `demos/`) |
| [demos/](demos/) | 8 reproducible top-venue paper figure scripts (house style) |
| [examples/](../examples/) | runnable examples in this repo |

Open `references/` only as needed; don't preload every file. Start from the table
above, then follow the internal links (and `demos/`, `examples/` scripts).

## License and attribution

- **scifig package + examples**: authored in this repo, MIT.
- **demos/ + reference methodology**: from
  [figures4papers](https://github.com/ChenLiu-1996/figures4papers) (author
  **Chen Liu**, Yale), **CC BY-NC 4.0** (non-commercial; see upstream LICENSE,
  this repo's LICENSE and NOTICE.md).
- **assets/*.mplstyle**: derived from the personal `modern-matplotlib` /
  `scientific_publication` styles.

> Important: figures4papers' LICENSE is actually **CC BY-NC 4.0** (not MIT).
> This repo's LICENSE (MIT) covers only the `scifig` package and `examples/`;
> `demos/` and the derived reference text remain under upstream CC BY-NC 4.0.
> Check before commercial use.
