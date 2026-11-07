# scifig

**Publication-grade scientific figures**: a thin matplotlib harness with your two
preferred styles and **pure-Python panel composition + annotation**.

> Use `apply_publication_style` for paper figures, `apply_modern_style` for
> slides/reports. The style lives entirely in the package; your code writes only
> data. Combining panels, adding panel letters, shared legends, insets, and
> significance brackets all happen in Python — no Illustrator.

## Layout

```
scifig/          Python package (styles + plot helpers + compose/annotate)
  style.py       apply_publication_style / apply_modern_style / create_subplots / finalize_figure
  palette.py     PALETTE / DEFAULT_COLORS / MODERN_COLORS / COLORBLIND_SAFE
  helpers.py     make_grouped_bar / make_trend / make_heatmap / make_scatter / make_sphere_illustration
  compose.py     panel_grid / join_figures / add_panel_label / shared_legend / add_inset / add_sig
  assets/        scientific_publication.mplstyle + modern.mplstyle (bundled; no hard-coded paths)
skill/           Agent skill (SKILL.md + references/ + demos/)
examples/        runnable example scripts
```

## Install

```bash
pip install -e .
# or: pip install -r requirements.txt
```

## Quick start

```python
import matplotlib
matplotlib.use("Agg")          # headless / batch
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=18))
fig, ax = scifig.create_subplots(1, 1)
scifig.make_grouped_bar(
    ax, ["A", "B", "C"], [[0.9, 0.8, 0.7], [0.7, 0.6, 0.5]],
    ["Ours", "Baseline"], ylabel="Score", annotate=True,
)
scifig.finalize_figure(fig, "out/fig")   # -> out/fig.pdf (vector-first)
```

Or by path only: `plt.style.use(...scifig/assets/scientific_publication.mplstyle)`
without importing the package.

## Pure-Python compose + annotate

```python
import scifig

# Stitch two saved PDF/PNG panels into one 1x2 figure, add lowercase letters (Nature)
fig, axes = scifig.join_figures(["a.pdf", "b.pdf"], labels=["a", "b"])
scifig.finalize_figure(fig, "out/combo")   # vector PDF by default

# Or build a grid in one figure, share the legend, add a significance bracket
fig, axes = scifig.panel_grid(1, 2)
scifig.make_trend(axes[0], epochs, [acc_a, acc_b], ["Model A", "Model B"])
scifig.add_sig(axes[0], 0, 1, y=0.95, marker="***")
scifig.shared_legend(fig, location="upper center")
```

## Nature / Science conventions

- **Nature**: panel letters are **lowercase** `a, b, c`
  (`add_panel_labels(case="lower")`); body text **Arial 5-6pt**; column widths
  single 3.50in, half 5.00in, double/full 7.20in.
- **Science**: panel letters are **uppercase bold** **A, B, C** (default
  `case="upper"`).
- **Vector-first**: `finalize_figure` emits the **vector PDF** by default
  (editable text, infinitely scalable); PNG is raster — only for screen previews.

```python
import scifig
scifig.apply_publication_style(scifig.nature_single_style(font_size=6.0))  # Arial 6pt, thin spines
fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("single"))  # 3.5in wide
scifig.finalize_figure(fig, "out/panel")   # -> out/panel.pdf
```

See **`examples/`** for runnable scripts (`grouped_bar.py`, `trends_grid.py`,
`heatmap.py`, `compose_annotate.py`, `full_multipanel.py`).

## Agent skill

`skill/` is the agent skill for this repo. Reference it by path
(`skill/SKILL.md`, plus `references/api.md`, `design-theory.md`, `cookbook.md`
as needed), or symlink it: `ln -s "$(pwd)/skill" ~/.agents/skills/scifig`.

## Styles / palettes

| Name | Use | Entry point |
|------|-----|-------------|
| `scientific_publication` | paper figures (Arial, thin spines, vector) | `apply_publication_style()` |
| `modern` | slides / web | `apply_modern_style()` |
| `PALETTE` | semantic colors (blue=method, green=improvement, red=baseline, neutral=background) | `scifig.PALETTE` |

## License (important)

- **MIT**: this repo's `scifig/` package and `examples/`.
- **CC BY-NC 4.0 (non-commercial)**: `skill/demos/figure_*` and the
  `skill/references/` methodology, from
  [figures4papers](https://github.com/ChenLiu-1996/figures4papers) (author
  **Chen Liu**, Yale). The upstream LICENSE is **CC BY-NC 4.0, not MIT** —
  corrected in this repo's LICENSE / NOTICE.md. Check before commercial use.

See `LICENSE` and `NOTICE.md`.
