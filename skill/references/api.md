# scifig API (the `_house` helpers)

There is no scifig package. The reusable interface is the small local module
`examples/_house.py` used by the example recipes. Copy the pieces you need into
your own script (the same code is given as copy-paste in
[house-style.md](house-style.md)).

## style(font_size=6.0, axes_linewidth=0.8, font=None)

Apply the publication house style (call once, before creating figures). Sets
Arial ~5-6pt, thin spines, readable/minor ticks, editable vector text
(`pdf.fonttype=42`), exact-size save (`savefig.bbox=standard`), no grid.

## figsize(width='single', aspect=0.75)

Physical figure size in inches: `single` 3.50, `half` 5.00, `double` 7.20.

## palette_labels(labels, ours_marker=None)

Semantic colors: label containing `ours_marker` is blue; others cycle
blue/red/green/teal/violet/neutral.

## save(fig, out, formats=('pdf',), dpi=600)

Vector-first save. Writes `out.pdf` (default); add `'png'` for a preview.

## finish(ax, grid=False, xlabel=None, ylabel=None, title=None)

One-call polish: labels, readable/minor ticks, optional subtle grid behind data.

## panel_label(ax, letter) / panel_letters(axes, case='lower')

Panel letter at the top-left corner (outside the axes).

## bar_labels(ax, bars, fmt='{:.2f}', pad=3)

Value labels above bars. `readable_ticks(ax, n=5)` sets deliberate tick density.

## Plot builders

| Builder | Signature |
|---------|-----------|
| `grouped_bar` | `(ax, categories, series, labels, ylabel, colors, ours_marker, annotate, yerr, capsize, hide_xticks)` |
| `trend` | `(ax, x, ys, labels, colors, ours_marker, ylabel, xlabel, show_shadow)` — 2-col `(mean, std)` series draws a CI band |
| `heatmap` | `(ax, matrix, x_labels, y_labels, cmap, cbar_label, annotate)` |
| `scatter` | `(ax, x, y, label, color, size, alpha)` |
| `boxplot` | `(ax, data, labels, palette, ylabel, widths)` |
| `pie` | `(ax, values, labels, colors, startangle, counterclock, pct)` |
| `scatter_fit` | `(ax, x, y, degree, label, color, fit)` — +95% CI band |
| `roc_curve` | `(ax, y_true, y_score, label, color)` — +AUC (no sklearn) |
| `confusion` | `(ax, cm, labels, cmap)` — annotated |
| `stacked_bar` | `(ax, categories, parts, labels, colors, ylabel)` — legend above |
| `grid` | `(nrows, ncols, width, aspect, wspace, hspace)` → `(fig, axes_flat)` |
| `shared_legend` | `(fig, labels, handles, location, ncol, clear)` |
| `join_figures` | `(files, out, ncols, labels, dpi)` — stitch saved panels |
| `add_sig` | `(ax, x0, x1, y, marker, height)` — significance bracket |
| `add_inset` | `(ax, loc, size)` → inset axes |

## Domain recipes (in `examples/`)

* `examples/biofigs.py` — `volcano`, `ma_plot`, `dot_plot`, `umap_scatter`,
  `violin_groups`.
* `examples/proteinfig.py` — `pymol_cartoon` (PyMOL, raster PNG),
  `matplotlib_cartoon` (real PDB coords + SSE, vector PDF).

## Universal rules (every figure)

Arial ~5-6pt; semantic colors; thin spines; units + N + uncertainty; vector-first
PDF; reproducible (data from a path); verify before claiming done.

## Related

- [house-style.md](house-style.md) — copy-paste style + helpers
- [capability-spec.md](capability-spec.md) — what figure types are covered
- [templates.md](templates.md) — figure-type templates
- [figure-guidelines.md](figure-guidelines.md) — agent workflow (ask-first)
