#!/usr/bin/env python3
"""Multi-panel trends with ONE shared legend (no per-panel duplication)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, grid, trend, add_sig, finish, save

style(font_size=6.0, axes_linewidth=0.8)
fig, axes = grid(1, 3, width="double", aspect=0.32)

x = np.linspace(0, 10, 50)
y1 = 0.5 + 0.4 * (1 - np.exp(-x / 3))
y2 = 0.45 + 0.35 * (1 - np.exp(-x / 4))

for ax, title, series in zip(
    axes,
    ["Training", "Validation", "Inference"],
    [[y1, y2], [y1 * 1.05, y2 * 1.02], [y1, y2]],
):
    trend(ax, x, series, ["Model A", "Model B"], ylabel="Score", xlabel="Step")
    ax.get_legend().remove()          # drop per-panel legend (use the shared one)
    ax.set_title(title, pad=4)
    finish(ax, grid=False)

# ONE shared legend above the panels
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
fig.subplots_adjust(top=0.82)
# significance bracket on the first panel (a clear difference at early steps)
add_sig(axes[0], 0.0, 1.0, y=0.72, marker="**", height=0.04)

save(fig, "out/trends_grid", formats=("pdf", "png"), dpi=300)
print("wrote out/trends_grid.pdf/png")
