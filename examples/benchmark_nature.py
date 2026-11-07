#!/usr/bin/env python3
"""Realistic benchmark figure sized to a Nature full-page (double-column) width.

Simulates a real multimodal model benchmark: grouped accuracy bars a, training
curves with uncertainty bands b, latency-vs-accuracy scatter c, feature
correlation heatmap d, ablation bars e, and a training/validation trend f.
Uses Arial ~7pt text, thin spines, lowercase Nature panel letters, vector PDF.
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scifig

np.random.seed(7)


def mock_accuracy(seed, n):
    rng = np.random.default_rng(seed)
    return np.clip(0.55 + 0.35 * rng.random(n), 0, 1)


def main():
    style = scifig.FigureStyle(font_size=7.0, axes_linewidth=0.8)
    scifig.apply_publication_style(style)

    # Nature full-page width (7.20in); panel_grid reserves a bottom legend strip
    fig, axes = scifig.panel_grid(2, 3, figsize=(7.20, 7.20 * 0.52),
                                  legend="bottom", legend_height=0.06)
    ax_a, ax_b, ax_c, ax_d, ax_e, ax_f = axes

    # --- a) grouped accuracy bars across 4 benchmark tasks ---
    tasks = ["MMI", "VQA", "OCR", "Chart"]
    ours = [0.92, 0.88, 0.85, 0.90]
    base = [0.82, 0.79, 0.80, 0.84]
    rng = np.random.default_rng(1)
    ours = np.array(ours) + rng.normal(0, 0.015, 4)
    base = np.array(base) + rng.normal(0, 0.015, 4)
    scifig.make_grouped_bar(
        ax_a, tasks, [ours, base], ["Our method", "Fine-tuned baseline"],
        ylabel="Accuracy",
        colors=[scifig.PALETTE["blue_main"], scifig.PALETTE["neutral"]],
    )
    ax_a.set_ylim(0.75, 1.00)

    # --- b) training curves with uncertainty bands (3 models) ---
    steps = np.linspace(0, 50, 60)
    curves = []
    for base_acc, col in [(0.86, "blue_main"), (0.80, "green_3"), (0.74, "red_strong")]:
        mean = base_acc - 0.35 * np.exp(-steps / 18)
        std = 0.02 + 0.01 * np.exp(-steps / 10)
        curves.append(np.stack([mean, std], axis=1))
    scifig.make_trend(ax_b, steps, curves, ["Ours", "Baseline X", "Baseline Y"],
                      ylabel="Validation accuracy", xlabel="Epoch",
                      colors=[scifig.PALETTE[k] for k in ("blue_main", "green_3", "red_strong")])
    ax_b.set_ylim(0.35, 0.92)

    # --- c) latency vs accuracy scatter ---
    lat = np.array([10, 12, 15, 18, 22, 27, 33, 40, 48, 58, 70, 84, 100])
    acc = 0.55 + 0.32 * (1 - np.exp(-(lat - 8) / 22)) + rng.normal(0, 0.01, lat.size)
    scifig.make_scatter(ax_c, lat, acc, label="Model Config", size=28,
                        color=scifig.PALETTE["teal"], alpha=0.85)
    # Pareto-ish trend
    xx = np.linspace(lat.min(), lat.max(), 100)
    scifig.make_trend(ax_c, xx, [[0.55 + 0.32 * (1 - np.exp(-(xx - 8) / 22))]], [],
                      color=scifig.PALETTE["red_strong"], ylabel="Accuracy", xlabel="Latency (ms)")
    ax_c.set_xscale("log")

    # --- d) feature correlation heatmap ---
    feats = ["Image", "Text", "OCR", "Chart", "Audio", "Video"]
    # build a plausible positive-definite-ish correlation matrix
    raw = rng.normal(0, 1, (6, 6))
    corr = raw @ raw.T / 6
    corr = 0.6 * corr / np.max(np.abs(corr))
    np.fill_diagonal(corr, 1.0)
    scifig.make_heatmap(ax_d, corr, x_labels=feats, y_labels=feats, cmap="RdBu_r",
                        cbar_label="Pearson r")

    # --- e) ablation bars ---
    abl = ["Full", "No OCR", "No Chart", "No Audio", "No pretrain"]
    scores = [0.92, 0.86, 0.84, 0.88, 0.71]
    scifig.make_grouped_bar(ax_e, abl, [scores], ["Ablation"],
                            ylabel="Accuracy",
                            colors=[scifig.PALETTE["blue_secondary"]],
                            annotate=True)
    ax_e.set_ylim(0.6, 1.0)

    # --- f) training vs validation with significance bracket ---
    train = 0.9 - 0.45 * np.exp(-steps / 12)
    valid = 0.86 - 0.35 * np.exp(-steps / 18)
    scifig.make_trend(ax_f, steps, [train, valid], ["Train", "Valid"],
                      ylabel="Accuracy", xlabel="Epoch",
                      colors=[scifig.PALETTE["blue_main"], scifig.PALETTE["violet"]])
    scifig.add_sig(ax_f, 0, 1, y=0.90, marker="***")
    ax_f.set_ylim(0.35, 0.95)

    # Lowercase Nature panel letters; single shared legend in the reserved strip
    scifig.add_panel_labels(axes, case="lower")
    scifig.shared_legend(fig, location="lower center", ncol=3, handlelength=1.2)

    scifig.finalize_figure(fig, "out/benchmark_nature", formats=["pdf", "png"], dpi=600)
    print("wrote out/benchmark_nature.pdf (vector) + .png (preview)")


if __name__ == "__main__":
    main()
