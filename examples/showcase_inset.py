#!/usr/bin/env python3
"""Inset-figure: a bio panel with the vector protein cartoon inserted.

Demonstrates scifig's inset capability: a protein topology is inserted into a
larger differential-expression figure using ``add_inset``. Because the cartoon
is pure matplotlib, the whole composite stays **vector** (PDF/SVG) — nothing is
rasterised, unlike inserting a PyMOL PNG.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

rng = np.random.default_rng(1)
log2fc = rng.normal(0, 1.1, 1500)
pval = np.clip(np.exp(-np.abs(log2fc) * 1.2) + rng.uniform(0, 0.2, 1500), 1e-12, 1.0)

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.5, axes_linewidth=0.8))
fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("double", aspect=0.52))

# main panel: volcano
scifig.volcano(ax, log2fc, pval, fc_thresh=1.0, p_thresh=0.05)

# inset: vector protein cartoon (top-left), proves vector insertion
ax_in = scifig.add_inset(ax, "upper left", size="28%")
coords = scifig.demo_structure()
sse = "h" * 240 + "e" * 80
scifig.draw_topology(ax_in, coords, sse=sse, color=scifig.PALETTE["blue_main"])
ax_in.set_xticks([]); ax_in.set_yticks([])
ax_in.set_xlabel(""); ax_in.set_ylabel("")

fig.tight_layout(pad=1)
scifig.finalize_figure(fig, "out/showcase_inset", formats=["pdf", "png"], dpi=600)
print("wrote out/showcase_inset.pdf/png (vector inset protein)")
