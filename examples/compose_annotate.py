#!/usr/bin/env python3
"""Compose two separate figure files into one multi-panel figure + panel letters."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=12))

# --- Panel A: a trend ---
fig_a, ax_a = scifig.create_subplots(1, 1)
x = np.linspace(0, 10, 50)
scifig.make_trend(ax_a, x, [0.9 - 0.3 * np.exp(-x / 3)], ["Model"], ylabel="Score")
scifig.finalize_figure(fig_a, "out/_panel_a", formats=["png"], dpi=200)

# --- Panel B: a scatter ---
fig_b, ax_b = scifig.create_subplots(1, 1)
scifig.make_scatter(ax_b, x, x * 0.7 + 0.1, label="Samples")
scifig.finalize_figure(fig_b, "out/_panel_b", formats=["png"], dpi=200)

# --- Compose into one 1x2 figure with panel letters ---
fig, axes = scifig.join_figures(["out/_panel_a.png", "out/_panel_b.png"], labels=["A", "B"])
scifig.finalize_figure(fig, "out/composed", formats=["png"], dpi=200, close=False)
print("wrote out/composed.png")
