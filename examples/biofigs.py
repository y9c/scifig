"""Domain figures (reference implementations) — plain matplotlib + house style.

These are **examples**: they show how to compose publication-quality
bioinformatics figures from the scifig house style and the `_house` helpers.
An agent reads these and re-implements or extends them in the user's env.

Covered: volcano, MA plot, marker dot plot, UMAP scatter, per-group violin.
"""

from __future__ import annotations

import numpy as np

from _house import PALETTE, FRIENDLY

# Semantic up / down / not-significant colors.
SIGNIFICANT_SCHEME = {
    "up": PALETTE["red_strong"],
    "down": PALETTE["blue_main"],
    "ns": PALETTE["neutral"],
}


def volcano(ax, log2fc, pval, gene_names=None, fc_thresh=1.0, p_thresh=0.05,
            label_top=8, xlabel="log2 fold change", ylabel="-log10(p-value)"):
    """Volcano plot: log2FC (x) vs -log10 p (y), up/down/n.s. colored."""
    fc = np.asarray(log2fc, float)
    p = np.asarray(pval, float)
    if np.any(p <= 0):
        p = np.where(p <= 0, np.nanmin(p[p > 0]) / 10, p)
    neg = -np.log10(p)
    up = (fc > fc_thresh) & (p < p_thresh)
    down = (fc < -fc_thresh) & (p < p_thresh)
    ns = ~(up | down)
    ax.scatter(fc[ns], neg[ns], s=8, c=SIGNIFICANT_SCHEME["ns"], alpha=0.5, linewidths=0)
    ax.scatter(fc[down], neg[down], s=10, c=SIGNIFICANT_SCHEME["down"], alpha=0.8, linewidths=0)
    ax.scatter(fc[up], neg[up], s=10, c=SIGNIFICANT_SCHEME["up"], alpha=0.8, linewidths=0)
    ax.axvline(-fc_thresh, color="0.4", ls="--", lw=0.6)
    ax.axvline(fc_thresh, color="0.4", ls="--", lw=0.6)
    ax.axhline(-np.log10(p_thresh), color="0.4", ls="--", lw=0.6)
    if gene_names is not None and label_top:
        sig = np.where(up | down)[0]
        sig = sig[np.argsort(-np.abs(fc[sig]))[:label_top]]
        for i in sig:
            ax.text(fc[i], neg[i], gene_names[i], fontsize=5.5, ha="center", va="bottom")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


def ma_plot(ax, mean_expr, log2fc, pval=None, fc_thresh=1.0, p_thresh=0.05,
            xlabel="mean normalized expression", ylabel="log2 fold change"):
    """MA plot: mean expression vs log2 fold change."""
    m = np.asarray(mean_expr, float)
    fc = np.asarray(log2fc, float)
    if pval is not None:
        up = (fc > fc_thresh) & (np.asarray(pval) < p_thresh)
        down = (fc < -fc_thresh) & (np.asarray(pval) < p_thresh)
        ns = ~(up | down)
        ax.scatter(m[ns], fc[ns], s=6, c=SIGNIFICANT_SCHEME["ns"], alpha=0.5, linewidths=0)
        ax.scatter(m[down], fc[down], s=8, c=SIGNIFICANT_SCHEME["down"], alpha=0.8, linewidths=0)
        ax.scatter(m[up], fc[up], s=8, c=SIGNIFICANT_SCHEME["up"], alpha=0.8, linewidths=0)
    else:
        ax.scatter(m, fc, s=6, c=PALETTE["blue_main"], alpha=0.6, linewidths=0)
    ax.axhline(0, color="0.4", lw=0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


def dot_plot(ax, expression, genes, clusters, pct=None, cmap="viridis",
             size_range=(8, 60), cbar_label="scaled expression"):
    """Single-cell marker dot plot: colour = expression, size = % expressed."""
    m = np.asarray(expression, float)
    n_g, n_c = m.shape
    size_src = np.asarray(pct, float) if pct is not None else m
    X, Y = np.meshgrid(np.arange(n_c), np.arange(n_g))
    smin, smax = size_src.min(), size_src.max()
    size = (size_src - smin) / (smax - smin) if smax > smin else np.zeros_like(size_src)
    size_px = size_range[0] + (size_range[1] - size_range[0]) * size
    sc = ax.scatter(X.ravel(), Y.ravel(), s=size_px.ravel(), c=m.ravel(),
                    cmap=cmap, linewidths=0.4, edgecolor="white")
    ax.set_xticks(np.arange(n_c))
    ax.set_xticklabels(clusters, rotation=40, ha="right")
    ax.set_yticks(np.arange(n_g))
    ax.set_yticklabels(genes)
    ax.figure.colorbar(sc, ax=ax, shrink=0.8, label=cbar_label)
    return ax


def umap_scatter(ax, x, y, labels, palette="tol_bright", size=14, alpha=0.75,
                 xlabel="UMAP-1", ylabel="UMAP-2"):
    """UMAP-style 2-D embedding colored by cluster."""
    labels = np.asarray(labels)
    pal = FRIENDLY.get(palette, FRIENDLY["wong"])
    for i, c in enumerate(dict.fromkeys(labels)):
        m = labels == c
        ax.scatter(np.asarray(x)[m], np.asarray(y)[m], s=size, alpha=alpha,
                   c=pal[i % len(pal)], linewidths=0, label=str(c))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, fontsize=6, loc="best")
    return ax


def violin_groups(ax, data, groups=None, palette="tol_bright", order=None,
                  ylabel="Expression", showmeans=True):
    """Per-group distribution (violin) for a numeric vector grouped by a label."""
    data = np.asarray(data, float)
    if groups is None:
        groups = np.zeros(len(data))
    groups = np.asarray(groups)
    uniq = list(dict.fromkeys(groups)) if order is None else list(order)
    parts = [data[groups == c] for c in uniq]
    pal = FRIENDLY.get(palette, FRIENDLY["wong"])
    bp = ax.violinplot(parts, showmeans=showmeans, showextrema=True, showmedians=True)
    for i, body in enumerate(bp["bodies"]):
        body.set_facecolor(pal[i % len(pal)])
        body.set_alpha(0.7)
        body.set_edgecolor("black")
    if "cmedians" in bp:
        bp["cmedians"].set_color("black")
    ax.set_xticks(np.arange(1, len(uniq) + 1))
    ax.set_xticklabels([str(c) for c in uniq], rotation=30, ha="right")
    ax.set_ylabel(ylabel)
    return ax
