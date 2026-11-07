#!/usr/bin/env python3
"""Multi-panel trends with a shared legend + significance annotation."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=14, axes_linewidth=2))
fig, axes = scifig.panel_grid(1, 3, figsize=(14, 4))

x = np.linspace(0, 10, 50)
y1 = 0.5 + 0.4 * (1 - np.exp(-x / 3))
y2 = 0.45 + 0.35 * (1 - np.exp(-x / 4))

scifig.make_trend(axes[0], x, [y1, y2], ["Model A", "Model B"], ylabel="Score", xlabel="Step")
axes[0].set_title("Training")
scifig.make_trend(axes[1], x, [y1 * 1.05, y2 * 1.02], ["Model A", "Model B"], ylabel="Score", xlabel="Step")
axes[1].set_title("Validation")

ns_ = np.linspace(0, 10, 50)
scifig.make_trend(axes[2], ns_, [y1, y2], [], ylabel="Score", xlabel="Step")
axes[2].set_title("Inference")
del ns_

# shared legend across all panels, significance bracket on panel A
scifig.shared_legend(fig, location="upper center", ncol=2)
scifig.add_sig(axes[0], 0, 0.5, y=0.80, marker="*")

scifig.finalize_figure(fig, "out/trends_grid", formats=["png", "pdf"], dpi=300)
print("wrote out/trends_grid.png/pdf")
