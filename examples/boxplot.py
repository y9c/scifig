#!/usr/bin/env python3
"""Box plot: per-group distribution comparison (house style)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, boxplot, save, finish

rng = np.random.default_rng(0)
style()
fig, ax = plt.subplots(figsize=(3.5, 2.9))

groups = ["Control", "Drug A", "Drug B"]
data = [rng.normal(5.0, 1.0, 80),
        rng.normal(6.2, 1.1, 80),
        rng.normal(4.6, 0.9, 80)]

boxplot(ax, data, labels=groups, ylabel="Score (a.u.)")
finish(ax, grid=False)
save(fig, "out/boxplot", dpi=600)
print("wrote out/boxplot.pdf")
