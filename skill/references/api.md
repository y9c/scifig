# scifig API Reference

This is the reference for the `scifig` package in this repository. It implements the
conventions once specified abstractly (figures4papers methodology) as a small,
importable harness. Import all public symbols from the top-level package:

```python
import scifig
```

Everything below is confirmed against `scifig/__init__.py` and the module docstrings.

---

## Constants

### PALETTE (semantic)

```python
scifig.PALETTE = {
    "blue_main": "#0F4D92", "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",
    "red_1": "#F6CFCB", "red_2": "#E9A6A1", "red_strong": "#B64342",
    "neutral": "#CFCECE", "highlight": "#FFD700",
    "teal": "#42949E", "violet": "#9A4D8E",
}
```

Blues = proposed/key method; greens = improvements; reds = baselines/contrasts;
neutral = background; highlight = single callout.

### Default color sequences

- `scifig.DEFAULT_COLORS` = `[blue_main, green_3, red_strong, teal, violet, neutral]`
  (used when `colors` is not passed to the `make_*` helpers).
- `scifig.MODERN_COLORS`, `scifig.COLORBLIND_SAFE` — categorical families for the
  modern / colorblind palettes (see `palette.py`).

---

## Style

Apply a style **once, before creating figures**. Both are idempotent and set
rcParams globally via matplotlib.

### scifig.FigureStyle

```python
@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 16
    axes_linewidth: float = 2.5
    use_tex: bool = False
    font_family: tuple[str, ...] = ("DejaVu Sans", "Helvetica", "Arial", "sans-serif")
```

### apply_publication_style(style=None)

Loads the bundled `scientific_publication.mplstyle`, then overrides: spines
top/right off, frameless legend, `svg.fonttype='none'`, and the `FigureStyle`
knobs (`font_size`, `axes_linewidth`, `use_tex`, `font_family`).

```python
scifig.apply_publication_style(scifig.FigureStyle(font_size=24, axes_linewidth=3))
```

### apply_modern_style()

Loads the bundled `modern.mplstyle` (presentation/web look).

### set_palette(name)

Sets `axes.prop_cycle`. Options: `'publication'`, `'modern'` (default),
`'colorblind'`, `'dark'`, `'pastel'`.

---

## Figure lifecycle

### create_subplots(nrows=1, ncols=1, figsize=None, **kwargs)

Returns `(fig, axes)` with `axes` flattened to 1D (a single `Axes` for 1x1).

### finalize_figure(fig, out_path, formats=None, dpi=300, close=True, pad=0.05, **kwargs)

Saves to one or more formats. `formats=None` → uses `out_path`'s extension, else
`['pdf','svg','eps']`. Creates parent dirs. Returns `list[Path]`. Defaults:
`bbox_inches='tight'`, `pad_inches=pad`, `facecolor='white'`.

### style_axis(ax, ...)

Modern axis polish (spines off, grid). Mutates and returns `ax`.

### make_figure(figsize=(10,6), nrows=1, ncols=1, **kwargs)

`apply_modern_style()` + `plt.subplots`. Convenience for the modern path.

### save_figure(fig, filename, formats=None, **kwargs) / set_hidpi(dpi=200)

Legacy helpers from the original style_helper: multi-format save; retina DPI.

---

## Plot helpers

All mutate the given `Axes` and return whatever is useful.

### make_grouped_bar(ax, categories, series, labels, ylabel='Value', colors=None, annotate=False, **bar_kw)

`categories`: x labels; `series`: list of arrays, each length == `len(categories)`;
`labels`: legend labels. Returns the last `BarContainer` (feed to `annotate_bars`).
Raises if lengths mismatch. `annotate=True` calls `annotate_bars` on the last series.

### annotate_bars(ax, bars, fmt='{:.2f}', fontsize=10, padding=3)

Value labels above each bar in a `BarContainer`; skips nan bars.

### make_trend(ax, x, y_series, labels, colors=None, ylabel=None, xlabel=None, show_shadow=True, linestyles=None, **plot_kw)

Each series is 1D (plain) **or** an `(N,2)` array `(mean, std)`. With `show_shadow`
and a 2-col series, an alpha `fill_between` uncertainty band is drawn. Returns the
`Line2D` list. Legend added (frameless).

### make_heatmap(ax, matrix, x_labels=None, y_labels=None, cmap='magma', cbar_label=None, annotate=False, fmt='{:.2f}')

2D matrix, optional labels, colorbar with label, optional cell annotations. Returns `im`.

### make_scatter(ax, x, y, label=None, color=None, size=50, alpha=0.7, **kw)

Same-length 1D `x`,`y`. Returns the `PathCollection`.

### make_sphere_illustration(ax, light_dir=(-0.5,0.5,0.8), resolution=128, alpha=0.6, radius=0.9, center=(0,0))

Shaded 2D disk mimicking a 3D sphere (grayscale `bone` shading). Turn off the axis.

---

## Compose & annotate (pure Python join)

The user-facing layer: combine several panels and annotate them without leaving Python.

### panel_grid(nrows, ncols, figsize=None, **kwargs)

`(fig, axes)` as a flat 1D array, normal GridSpec spacing.

### join_axes(axes, labels=None, figsize=None, wspace=0.18, hspace=0.22)

Reposition already-drawn axes onto one grid figure and (optionally) add panel letters.

### join_figures(files, out_path=None, ncols=None, figsize=None, labels=None, dpi=300, pad=0.05)

Stitch existing saved figure files (PNG/PDF/SVG) into one matrix. Loads each as an
image and hides axes. `labels` adds panel letters. Returns `(fig, axes)`.

### add_panel_label(ax, letter='A', x=-0.12, y=1.06, fontsize=13, fontweight='bold')

Panel letter at the top-left of an axes.

### add_panel_labels(axes, labels=None)

Batch version; defaults to `A, B, C, ...`.

### shared_legend(fig, handles=None, labels=None, location='upper center', ncol=None, **kw)

One legend for all axes (dedupes by label).

### add_inset(ax, loc, size='30%', axes_kw=None, indicator=True)

Inset axes with an optional region indicator. Returns the inset `Axes`.

### add_bracket(ax, x0, x1, y, height=0.03, text=None, fontsize=10) / add_sig(ax, x0, x1, y, marker='***', height=0.03, fontsize=11)

Significance/difference brackets (optionally labelled, e.g. `***`).

---

## Validation and conventions

- Numeric sequences are coerced to `float` arrays and length/dimension checks are
  enforced (helpers raise `ValueError` on mismatch rather than silently mis-plot).
- `finalize_figure` supports pdf, svg, eps, png, jpg, jpeg, tif, tiff.
- In headless/batch runs set a non-interactive backend before importing pyplot,
  e.g. `matplotlib.use("Agg")`.
- By default `apply_publication_style` sets `svg.fonttype='none'` so vector text
  stays editable, and `use_tex` only when LaTeX is available.

## Related files

- [SKILL.md](../SKILL.md) — when to use this skill
- [cookbook.md](cookbook.md) — min-code recipes
- [design-theory.md](design-theory.md) — why the style is chosen
- [common-patterns.md](common-patterns.md) — layout & print-safe patterns
- [demos.md](demos.md) — canonical figures4papers scripts (this repo `demos/`)
- [tutorials.md](tutorials.md) — end-to-end walks
