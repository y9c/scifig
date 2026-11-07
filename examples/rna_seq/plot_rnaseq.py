#!/usr/bin/env python3
"""RNA-seq QC + gene-expression figure (2 panels)."""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
import numpy as np
from _house import style, grid, finish, panel_letters, save, grouped_bar
from rna_seq.data import build

d = build()

style(font_size=6.0, axes_linewidth=0.8)
fig, axes = grid(1, 2, width="double", aspect=0.42)

# a) reads per sample (bar + error)
grouped_bar(axes[0], d["samples"], [d["qc"]["reads"] / 1e6],
            ["Reads (M)"], ylabel="Reads (M)",
            colors=["#0F4D92"],
            yerr=np.array([1.5, 2.0, 1.4, 2.1]), capsize=3)
axes[0].set_ylim(0, 50)

# b) captured genes per sample
grouped_bar(axes[1], d["samples"], [d["qc"]["genes"]],
            ["Detected genes"], ylabel="Genes detected",
            colors=["#8BCF8B"])
axes[1].set_ylim(0, 20000)

panel_letters(axes, case="lower")
for a in axes:
    finish(a, grid=False)
axes[0].set_xticklabels(d["samples"], rotation=0)
fig.tight_layout(pad=0.8)
save(fig, "out/rna_seq", formats=("pdf", "png"), dpi=600)
print("wrote out/rna_seq.pdf/png")
