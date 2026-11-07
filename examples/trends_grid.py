#!/usr/bin/env python3
"""Multi-panel trends with a shared legend + significance annotation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, grid, trend, add_sig, finish, save

style(font_size=6.0, axes_linewidth=0.8)
fig, axes = grid(1, 3, width="double", aspect=0.34)

x = np.linspace(0, 10, 50)
y1 = 0.5 + 0.4 * (1 - np.exp(-x / 3))
y2 = 0.45 + 0.35 * (1 - np.exp(-x / 4))

# collect handles/labels from the first axes for the shared legend
for ax, title, series in zip(
    axes,
    ["Training", "Validation", "Inference"],
    [[y1, y2], [y1 * 1.05, y2 * 1.02], [y1, y2]],
):
    trend(ax, x, series, ["Model A", "Model B"], ylabel="Score", xlabel="Step")
    ax.set_title(title, pad=4)
    finish(ax, grid=False)

# shared legend (dedup) + significance bracket on the first panel
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
add_sig(axes[0], 0, 0.5, y=0.80, marker="*")

save(fig, "out/trends_grid", formats=("pdf", "png"), dpi=300)
print("wrote out/trends_grid.pdf/png")
