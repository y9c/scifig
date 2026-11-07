#!/usr/bin/env python3
"""Inset figure: a volcano panel with a vector protein cartoon inserted.

The protein topology is drawn with plain matplotlib (real PDB coords + SSE), so
the whole composite stays **vector** (PDF) — nothing rasterised, unlike inserting
a PyMOL PNG.
"""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt
import numpy as np
from _house import style, add_inset, save, finish
from biofigs import volcano
from proteinfig import matplotlib_cartoon

rng = np.random.default_rng(1)
# realistic DE: most genes near 0, a clear set up-regulated and down-regulated
log2fc = rng.normal(0, 0.4, 1500)
log2fc[:400] += rng.choice([-1.5, 1.5], 400) * (0.8 + rng.random(400))  # strong DE
log2fc[400:520] += rng.choice([-2.0, 2.0], 120) * rng.random(120)        # extreme DE
# p-value strongly tied to |effect| (so significant genes are visible)
pval = np.exp(-np.abs(log2fc) * 1.6)
pval = np.clip(pval + rng.uniform(0, 0.005, 1500), 1e-15, 1.0)

style(font_size=6.0, axes_linewidth=0.8)
fig, ax = plt.subplots(figsize=(7.2, 7.2 * 0.52))

# main panel: volcano
volcano(ax, log2fc, pval, fc_thresh=1.0, p_thresh=0.05)
finish(ax, grid=False)

# inset: vector protein cartoon (upper-left) — proves vector insertion
ax_in = add_inset(ax, "upper left", size="28%")
matplotlib_cartoon(ax_in, "1CRN")
ax_in.set_xticks([]); ax_in.set_yticks([])
ax_in.set_xlabel(""); ax_in.set_ylabel("")

save(fig, "out/showcase_inset", formats=("pdf", "png"), dpi=600)
print("wrote out/showcase_inset.pdf/png (vector inset protein)")
