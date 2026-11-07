#!/usr/bin/env python3
"""RNA-seq QC + gene-expression figure (2 panels)."""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # examples/
import numpy as np
import scifig
from rna_seq.data import build

d = build()

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.5, axes_linewidth=0.8))
fig, axes = scifig.panel_grid(1, 2, figsize=scifig.nature_figsize("double", aspect=0.42),
                             legend=None)

# a) reads per sample (bar + error) grouped by condition
scifig.make_grouped_bar(axes[0], d["samples"], [d["qc"]["reads"] / 1e6],
                        ["Reads (M)"], ylabel="Reads (M)",
                        colors=[scifig.PALETTE["blue_main"]],
                        yerr=np.array([1.5, 2.0, 1.4, 2.1]), capsize=3)
axes[0].set_ylim(0, 50)

# b) captured genes per sample
scifig.make_grouped_bar(axes[1], d["samples"], [d["qc"]["genes"]],
                        ["Detected genes"], ylabel="Genes detected",
                        colors=[scifig.PALETTE["green_3"]],)
axes[1].set_ylim(0, 20000)

scifig.add_panel_labels(axes, case="lower")
for a in axes:
    scifig.finish_axes(a, grid=False)
axes[0].set_xticklabels(d["samples"], rotation=0)
fig.tight_layout(pad=0.8)
scifig.finalize_figure(fig, "out/rna_seq", formats=["pdf", "png"], dpi=600)
print("wrote out/rna_seq.pdf/png")
