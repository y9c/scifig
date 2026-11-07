#!/usr/bin/env python3
"""Differential-expression figure: volcano + MA plot (2 panels).

Uses scifig bio helpers on the local synthetic data. Semantic up/down coloring,
thin spines, no grid, Nature-style lower-case letters, vector PDF.
"""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # examples/
import numpy as np
import scifig
from diff_exp.data import build
from biofigs import volcano, ma_plot

d = build()

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.5, axes_linewidth=0.8))
fig, axes = scifig.panel_grid(1, 2, figsize=scifig.nature_figsize("double", aspect=0.42),
                             legend=None)

volcano(axes[0], d["log2fc"], d["pval"], gene_names=d["gene"],
        fc_thresh=1.0, p_thresh=0.05, label_top=6)
ma_plot(axes[1], d["mean_expr"], d["log2fc"], d["pval"],
        fc_thresh=1.0, p_thresh=0.05)

scifig.add_panel_labels(axes, case="lower")
scifig.finish_axes(axes[0], grid=False)
scifig.finish_axes(axes[1], grid=False)
fig.tight_layout(pad=0.8)
scifig.finalize_figure(fig, "out/diff_exp", formats=["pdf", "png"], dpi=600)
print("wrote out/diff_exp.pdf/png")
