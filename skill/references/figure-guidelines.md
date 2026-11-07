# Figure-Generation Contract (agent-first)

This is the contract an agent follows to produce any scifig figure. It is the
single source of truth for **how** figures are made — read it before writing any
figure code. The agent is first-class: it reads this, makes decisions, and
produces a figure with no hand-tuning of rcParams or per-script style hacks.

## The two mandatory questions

Before any code, ask (or infer) these two from the user/context:

1. **What is the one-line claim?** (the figure must make a single, defensible
   point — Depth axis.)
2. **Target venue + column width?** (Nature single/half/double, or a named
   journal via `journal_style`.) This fixes figsize + font size + panel case.

## Fixed decision ladder

Follow top-down; each level narrows the code:

1. **Describe with `FigureSpec` + `render_spec`** (preferred). Declare panels as
   dicts; scifig enforces style, colors, legend, letters, polish.
2. **Pick an archetype** (`timeseries_ci`, `sorted_bar`, `grouped_bar`,
   `scatter_fit`, `heatmap`, `tornado`, `confusion`) if the shape matches.
3. **Fall back to raw helpers** only for a genuinely novel layout — and call
   `finish_axes` on the result.
4. Never hand-edit rcParams per script.

## The polish checklist (applied to EVERY figure)

These are the "human effort" details that separate journal-grade from
programmatic. `render_spec` applies most automatically; add the rest explicitly.

| Polish | Rule | Helper |
|--------|------|--------|
| Bar edges | thin dark edge on every bar (separation in print) | `make_grouped_bar` (auto) |
| Readable ticks | 4-6 major ticks, not matplotlib defaults | `ticks_readable` |
| Minor ticks | subtle minor ticks for a "edited" look | `add_minor_ticks` |
| Subtle grid | light grid *behind* data, or off | `soft_grid` / `grid=False` |
| Tight y-limits | emphasize the relevant band, not 0-based | `tight_ylim` |
| Bar value labels | well-offset, scaled font | `bar_value_labels` |
| Uncertainty | CI band with alpha, never a bare line | `make_trend` (auto) |
| Panel balance | equal margins, no stretched axes | `finish_figure` |

## Hard rules (mandatory)

- **Arial ~5-6pt** at final column width (Nature). Lowercase panel letters for
  Nature (`panel_case="lower"`), uppercase bold for Science.
- **Semantic colors**: `assign_colors(labels, ours_marker="...")` — blue=ours,
  green=improvement, red/neutral=baseline. Never hardcode hex in user code.
- **Colorblind + grayscale safe**: pair colors with distinct markers/linestyles
  when luminance overlaps; or use `friendly_pal(name)`.
- **Units + N + uncertainty** on the figure (axis labels carry units).
- **Vector-first**: PDF is the primary output; PNG only for screen preview.
- **Reproducible**: script reads data from a path; no inline data > ~20 rows;
  no AI-generated images.

## Sequence (the agent runs these in order)

1. Write the one-line claim + choose column width.
2. Build the `FigureSpec` (or pick archetype).
3. If publication-bound, call `journal_style(name)` or set `FigureStyle`
   (`font_size`, `axes_linewidth`).
4. `render_spec(spec, out_path)` → writes the vector PDF.
5. Run `check_figure(fig, axes)` — must have **no FAIL** before claiming done.
6. Rasterize (`pdftoppm -png -r 200 out.pdf check.png`) and **visually confirm**
   no overlap, no clipping, letters clear, legend placed.
7. Answer the four judgment axes (Depth · Elegance · Unimpeachable · Visible gap).

## Code-generation template

```python
"""<one-line claim>. Target: <venue> <column-width>."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

# 1) venue + size
scifig.apply_publication_style(scifig.FigureStyle(font_size=6.0, axes_linewidth=0.8))

# 2) describe the figure (or use an archetype)
spec = scifig.FigureSpec(
    width="double", aspect=0.40, ncols=3, panel_case="lower",
    panels=[
        dict(type="bar", categories=[...], series=[...],
             labels=[...], ours_marker="...", ylabel="...", ylim=(...)),
        dict(type="trend", x=..., ys=[...], labels=[...],
             ours_marker="...", ylabel="...", xlabel="..."),
        dict(type="heatmap", matrix=..., cmap="RdBu_r", cbar_label="..."),
    ],
)

# 3) render (vector PDF + optional PNG preview)
fig, axes = scifig.render_spec(spec, "out/fig", formats=["pdf", "png"], dpi=600)

# 4) quality gate
scifig.check_figure(fig, axes)
```

## Anti-patterns (never do)

- Default matplotlib colors, default ticks, default figure size.
- `plt.style.use` + per-script rcParams patching.
- `bbox_inches="tight"` on the final export (it silently changes the size;
  use `savefig.bbox="standard"` and pick the figsize up front).
- Chart types per panel that don't share the same palette/size/spine language.
- Stacked bars with white segment separators that read as clutter (prefer
  grouped or a single readable series).
- A legend that overlaps data or a colorbar label jammed into an axis label.

## Related

- [api.md](api.md) — exact function signatures
- [design-theory.md](design-theory.md) — why the style choices exist
- [common-patterns.md](common-patterns.md) — layout & print-safe patterns
- [../AGENT.md](../AGENT.md) — editing this repo, not making figures
