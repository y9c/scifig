#!/usr/bin/env python3
"""Compose two separate figure files into one multi-panel figure + panel letters."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, trend, scatter, join_figures, save

style(font_size=6.0, axes_linewidth=0.8)

x = np.linspace(0, 10, 50)
# Panel A: a trend
fig_a, ax_a = plt.subplots(figsize=(3.5, 2.6))
trend(ax_a, x, [0.9 - 0.3 * np.exp(-x / 3)], ["Model"], ylabel="Score")
save(fig_a, "out/_panel_a", formats=("png",), dpi=200)
plt.close(fig_a)

# Panel B: a scatter
fig_b, ax_b = plt.subplots(figsize=(3.5, 2.6))
scatter(ax_b, x, x * 0.7 + 0.1, label="Samples")
save(fig_b, "out/_panel_b", formats=("png",), dpi=200)
plt.close(fig_b)

# Compose into one 1x2 figure with panel letters
fig, _ = join_figures(["out/_panel_a.png", "out/_panel_b.png"], labels=["A", "B"],
                      out="out/composed")
print("wrote out/composed.png")
