# scifig Capability Spec (agent-facing)

scifig is **not** a library that implements every plotting type. It is a
**platform + standards + universal interface + capability spec**: the agent reads
this and the examples, then implements any figure itself. scifig guarantees the
*look and conventions*; the agent supplies the *figure logic*.

## What scifig provides (the platform)

| Concern | Interface |
|---------|-----------|
| House style | `apply_publication_style`, `apply_modern_style`, `FigureStyle` |
| Publication sizes | `nature_figsize`, `journal_style`/`journal_figsize`, `fig_size_mm` |
| Semantic colors | `assign_colors`, `PALETTE`, `friendly_pal` |
| Universal primitives | `make_grouped_bar`, `make_trend`, `make_heatmap`, `make_scatter` |
| Composition | `panel_grid`, `join_axes`, `join_figures`, `add_inset`, `shared_legend`, `add_sig` |
| Polish | `finish_axes`, `finish_figure`, `bar_value_labels`, `tight_ylim`, `ticks_readable` |
| Declarative | `FigureSpec` + `render_spec` (describe, scifig renders) |
| OO builder | `Figure` + typed `*Panel` |
| Vector-safe export | `finalize_figure` (PDF first, exact-size, editable text) |
| Quality gate | `check_figure`, `QUALITY_AXES` |
| Layout audit | `audit_layout` / `fix_layout` (no overlap, no excessive gaps) |

**Anything not in this table is the agent's job** — and the agent does it with
these primitives, following the conventions below.

## Universal rules (apply to every figure, whatever the type)

- Arial ~5-6pt at final column width; lowercase Nature letters / uppercase bold Science.
- Semantic colors (blue=key, green=improve, red=baseline); never hardcode hex.
- Thin spines, subtle-or-off grid, readable/minor ticks, panel letters at corner.
- Units + N + uncertainty on the figure.
- Vector-first: PDF primary; `pdf.fonttype=42`; `savefig.bbox=standard`.
- Reproducible: read data from a path; no inline data > ~20 rows.
- Run `check_figure` (no FAIL) + visually confirm before done.

## What figure types are covered (the capability map)

Each row says what's **built-in** (scifig provides it) vs **recipe** (the agent
builds it from primitives; a worked example exists). Recipes are the template the
agent reads and extends.

| Figure type | Provider | Example |
|-------------|----------|---------|
| Grouped / single bars | built-in | `examples/grouped_bar.py`, `immunostruct_ref.py` |
| Trend / curves + CI | built-in | `examples/trends_grid.py` |
| Heatmap + colorbar | built-in | `examples/heatmap.py` |
| Scatter | built-in | `examples/compose_annotate.py` |
| Multi-panel grid | built-in | `examples/nature_fullpage.py`, `full_multipanel.py` |
| Quantitative comparison (bars + error + right legend) | recipe | `examples/benchmark_parity.py` |
| Volcano / MA (diff. expression) | recipe | `examples/biofigs.py`, `examples/diff_exp/` |
| Marker dot plot / UMAP / violin (single-cell) | recipe | `examples/biofigs.py`, `examples/single_cell/` |
| RNA-seq QC bars | recipe | `examples/rna_seq/` |
| Protein cartoon (PyMOL, raster) | recipe | `examples/proteinfig.py`, `pymol_render_aicda.py` |
| Protein topology (matplotlib, vector) | recipe | `examples/proteinfig.py`, `showcase_protein.py` |

> **Built-in** = scifig function; **recipe** = the agent composes from
> primitives (a reference implementation lives in `examples/`). The agent reads
> the recipe, understands it, and adapts it — it is **not** a package feature.

## The universal interface pattern

Every figure, no matter the type, follows the same shape — this is the contract
that keeps output consistent:

```python
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.0, axes_linewidth=0.8))
fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("single"))

# ... any figure logic, using scifig primitives ...

scifig.finish_axes(ax, grid=False)
scifig.finalize_figure(fig, "out/fig")   # vector PDF
```

## Agent workflow (ask first, then implement)

1. **Ask up to 5 questions** (claim / venue+width / panels / data / chart type).
2. **Check the capability map**: built-in → use it; recipe → read & adapt it;
   none → compose from primitives.
3. **Apply the universal rules** (style, colors, polish, vector, gate).
4. Run `check_figure`; visually confirm; done.

## Extending (new figure types)

If a figure type isn't covered, add it as a **recipe** under `examples/` (a
self-contained script using scifig primitives), not as a new package function.
That keeps scifig lean: the platform stays stable; recipes grow.
