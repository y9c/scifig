---
name: scifig
description: copy-paste recipes for publication-grade matplotlib figures (no package). Use for paper/slide/report figures.
---

# scifig

Publication figures with plain matplotlib. No package.

## Setup (prove it runs first)

```bash
make venv
cd examples && ../.venv/bin/python grouped_bar.py   # -> out/grouped_bar.pdf
```

If you get the PDF, you're good.

## Make a figure

Copy the style from `references/house-style.md`. Pick the closest example in `examples/`, copy it, swap the data.

Recipes: bars / box / stacked / pie / trend+CI / heatmap / scatter+fit / ROC / confusion / survival / volcano / UMAP / dot / violin / protein / inset / multi-panel.

## Rules

- Arial ~6pt, lowercase Nature letters.
- blue=key, green=improve, red=baseline.
- save vector PDF (`savefig.bbox="standard"`).
- Ask first: claim? venue+width? panels? data?
- Re-open the figure before saying done — no overlap.
