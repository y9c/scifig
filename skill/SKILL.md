---
name: scifig
description: quick copy-paste recipes for publication-grade matplotlib figures (no package, no install). Use for paper/slide/report figures.
---

# scifig

Publication figures with plain matplotlib. No install. Copy, paste, run.

## 1. Style (copy once, top of every script)

From `references/house-style.md` — copy the **style preamble** + the `save`/`finish`/`panel_label` helpers.

## 2. Pick a recipe (copy + adapt)

| Figure | Example |
|--------|---------|
| bars | `examples/grouped_bar.py` |
| trend + CI | `examples/trends_grid.py` |
| heatmap | `examples/heatmap.py` |
| scatter + fit | `examples/scatter_fit.py` |
| box / stacked / pie | `examples/{boxplot,stacked_bar,pie}.py` |
| ROC / confusion | `examples/{roc,confusion}.py` |
| survival | `examples/survival.py` |
| volcano / UMAP / violin | `examples/biofigs.py`, `examples/single_cell/` |
| protein | `examples/proteinfig.py`, `examples/showcase_protein.py` |

## 3. Rules (short)

- Arial ~6pt, lowercase Nature letters.
- Colors: blue=key, green=improve, red=baseline.
- Vector PDF first (`savefig.bbox="standard"`).
- Readable ticks, thin spines, panel letter top-left.
- Verify: re-open the figure, no overlap.

## 4. Ask first

Ask: claim? venue+width? panels? data? Then implement.

---

Docs: `references/capability-spec.md` (what's covered), `references/figure-guidelines.md` (workflow), `references/api.md` (helpers), `references/templates.md`.
