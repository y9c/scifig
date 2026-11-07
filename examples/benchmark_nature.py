#!/usr/bin/env python3
"""Realistic 6-panel benchmark figure (house style, plain matplotlib).

Multi-panel results figure: grouped bars, training curves + CI, latency vs
accuracy, correlation heatmap, ablation bars, train/valid with significance.
Lowercase Nature letters, shared legend, vector PDF.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from _house import style, grid, grouped_bar, trend, scatter, heatmap, \
    panel_letters, save, finish, add_sig

rng = np.random.default_rng(1)
style(font_size=6.0, axes_linewidth=0.8)
fig, axes = grid(2, 3, width="double", aspect=0.52)
ax_a, ax_b, ax_c, ax_d, ax_e, ax_f = axes

# a) grouped accuracy bars
tasks = ["MMI", "VQA", "OCR", "Chart"]
ours = np.array([0.92, 0.88, 0.85, 0.90]) + rng.normal(0, 0.015, 4)
base = np.array([0.82, 0.79, 0.80, 0.84]) + rng.normal(0, 0.015, 4)
grouped_bar(ax_a, tasks, [ours, base], ["Ours", "Baseline"], ylabel="Accuracy")
ax_a.set_ylim(0.75, 1.00)

# b) training curves + CI
steps = np.linspace(0, 50, 60)
curves = []
for b in (0.86, 0.80, 0.74):
    mean = b - 0.35 * np.exp(-steps / 18)
    std = 0.02 + 0.01 * np.exp(-steps / 10)
    curves.append(np.stack([mean, std], axis=1))
trend(ax_b, steps, curves, ["Ours", "Baseline X", "Baseline Y"],
      ylabel="Validation accuracy", xlabel="Epoch")
ax_b.set_ylim(0.35, 0.92)

# c) latency vs accuracy
lat = np.array([10, 12, 15, 18, 22, 27, 33, 40, 48, 58, 70, 84, 100])
acc = 0.55 + 0.32 * (1 - np.exp(-(lat - 8) / 22)) + rng.normal(0, 0.01, lat.size)
scatter(ax_c, lat, acc, label="Config", size=28, alpha=0.85)
ax_c.set_xscale("log")
ax_c.set_xlabel("Latency (ms)"); ax_c.set_ylabel("Accuracy")

# d) correlation heatmap
feats = ["Image", "Text", "OCR", "Chart", "Audio", "Video"]
raw = rng.normal(0, 1, (6, 6))
corr = raw @ raw.T / 6
corr = 0.6 * corr / np.max(np.abs(corr))
np.fill_diagonal(corr, 1.0)
heatmap(ax_d, corr, x_labels=feats, y_labels=feats, cmap="RdBu_r", cbar_label="Pearson r")

# e) ablation bars
abl = ["Full", "No OCR", "No Chart", "No Audio", "No pretrain"]
grouped_bar(ax_e, abl, [[0.92, 0.86, 0.84, 0.88, 0.71]], ["Ablation"],
            ylabel="Accuracy", annotate=True)
ax_e.set_ylim(0.6, 1.0)

# f) train vs valid + significance
train = 0.9 - 0.45 * np.exp(-steps / 12)
valid = 0.86 - 0.35 * np.exp(-steps / 18)
trend(ax_f, steps, [train, valid], ["Train", "Valid"], ylabel="Accuracy", xlabel="Epoch")
add_sig(ax_f, 0, 1, y=0.90, marker="***")
ax_f.set_ylim(0.35, 0.95)

panel_letters(axes, case="lower")
for a in axes:
    finish(a, grid=False)

# shared legend
h, l = [], []
for a in axes:
    hh, ll = a.get_legend_handles_labels()
    for x, y in zip(hh, ll):
        if y not in l:
            l.append(y); h.append(x)
fig.legend(h, l, loc="lower center", ncol=3, frameon=False, handlelength=1.2)

save(fig, "out/benchmark_nature", formats=("pdf", "png"), dpi=600)
print("wrote out/benchmark_nature.pdf/png")
