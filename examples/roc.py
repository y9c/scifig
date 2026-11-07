#!/usr/bin/env python3
"""ROC curves with AUC for two models (no sklearn)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, roc_curve, save, finish

rng = np.random.default_rng(2)
style()
fig, ax = plt.subplots(figsize=(3.6, 3.3))

y_true = rng.integers(0, 2, 200)
# model A: decent; model B: better
score_a = y_true * 0.6 + rng.normal(0, 0.5, 200)
score_b = y_true * 0.85 + rng.normal(0, 0.4, 200)

roc_curve(ax, y_true, score_a, label="Model A", color="#0F4D92")
roc_curve(ax, y_true, score_b, label="Model B", color="#B64342")
finish(ax, grid=False)
save(fig, "out/roc", dpi=600)
print("wrote out/roc.pdf")
