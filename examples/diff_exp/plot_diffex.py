#!/usr/bin/env python3
"""Differential-expression figure: volcano + MA plot (2 panels).

Uses the biofigs recipe on local synthetic data; house style; vector PDF.
"""
import matplotlib
matplotlib.use("Agg")
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
import numpy as np
from _house import style, grid, finish, panel_letters, save
from biofigs import volcano, ma_plot
from diff_exp.data import build

d = build()

style(font_size=6.0, axes_linewidth=0.8)
fig, axes = grid(1, 2, width="double", aspect=0.42)

volcano(axes[0], d["log2fc"], d["pval"], gene_names=d["gene"],
        fc_thresh=1.0, p_thresh=0.05, label_top=6)
ma_plot(axes[1], d["mean_expr"], d["log2fc"], d["pval"],
        fc_thresh=1.0, p_thresh=0.05)

panel_letters(axes, case="lower")
for a in axes:
    finish(a, grid=False)

save(fig, "out/diff_exp", formats=("pdf", "png"), dpi=600)
print("wrote out/diff_exp.pdf/png")
