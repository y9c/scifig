#!/usr/bin/env python3
"""Scatter + least-squares fit + 95% CI band."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, scatter_fit, save, finish

rng = np.random.default_rng(1)
style()
fig, ax = plt.subplots(figsize=(3.6, 3.1))

x = rng.uniform(0, 10, 60)
y = 0.8 * x + 0.5 + rng.normal(0, 0.8, x.size)

scatter_fit(ax, x, y, degree=1, label="Samples", fit=True)
ax.set_xlabel("Dose (μM)"); ax.set_ylabel("Response")
ax.legend(frameon=False, fontsize=6)
finish(ax, grid=False)
save(fig, "out/scatter_fit", dpi=600)
print("wrote out/scatter_fit.pdf")
