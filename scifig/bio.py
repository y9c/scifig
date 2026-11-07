"""Bioinformatics figure helpers.

Domain-specific primitives for genomics / single-cell figures built on top of
the core helpers. Each returns the mutated ``Axes`` so it composes with the
house polish and ``FigureSpec``.

Covered: differential expression (volcano, MA plot, ranking), single-cell
(marker dot plot, UMAP-style colored scatter, per-cluster violin), and generic
bio palettes.
"""

from __future__ import annotations

import numpy as np

from .palette import PALETTE, friendly_pal

__all__ = [
    "volcano",
    "ma_plot",
    "dot_plot",
    "umap_scatter",
    "violin_groups",
    "SIGNIFICANT_SCHEME",
]

# Semantic colors for up / down / not-significant points.
SIGNIFICANT_SCHEME = {
    "up": PALETTE["red_strong"],
    "down": PALETTE["blue_main"],
    "ns": PALETTE["neutral"],
}


def _threshold_mask(log2fc, pval, fc_thresh=1.0, p_thresh=0.05):
    """Return (up, down, ns) boolean masks from log2FC and p-value arrays."""
    fc = np.asarray(log2fc, float)
    p = np.asarray(pval, float)
    up = (fc > fc_thresh) & (p < p_thresh)
    down = (fc < -fc_thresh) & (p < p_thresh)
    ns = ~(up | down)
    return up, down, ns


def volcano(ax, log2fc, pval, gene_names=None, fc_thresh=1.0, p_thresh=0.05,
            label_top=8, colors=None, xlabel="log2 fold change",
            ylabel="-log10(p-value)", **kw):
    """Volcano plot: log2FC (x) vs -log10 p-value (y).

    Points are colored up / down / not-significant using ``SIGNIFICANT_SCHEME``
    unless ``colors`` given. The top ``label_top`` significant genes (by abs
    log2FC) are labelled. ``fc_thresh``/``p_thresh`` set significance lines.
    """
    fc = np.asarray(log2fc, float)
    p = np.asarray(pval, float)
    if np.any(p <= 0):
        p = np.where(p <= 0, np.nanmin(p[p > 0]) / 10, p)
    neglogp = -np.log10(p)
    up, down, ns = _threshold_mask(fc, p, fc_thresh, p_thresh)
    scheme = colors or SIGNIFICANT_SCHEME
    ax.scatter(fc[ns], neglogp[ns], s=8, c=scheme["ns"], alpha=0.5, linewidths=0, label="n.s.")
    ax.scatter(fc[down], neglogp[down], s=10, c=scheme["down"], alpha=0.8, linewidths=0, label="down")
    ax.scatter(fc[up], neglogp[up], s=10, c=scheme["up"], alpha=0.8, linewidths=0, label="up")
    # significance thresholds
    ax.axvline(-fc_thresh, color="0.4", linestyle="--", linewidth=0.6)
    ax.axvline(fc_thresh, color="0.4", linestyle="--", linewidth=0.6)
    ax.axhline(-np.log10(p_thresh), color="0.4", linestyle="--", linewidth=0.6)
    # label top significant genes
    if gene_names is not None and label_top:
        sig_idx = np.where(up | down)[0]
        sig_idx = sig_idx[np.argsort(-np.abs(fc[sig_idx]))[:label_top]]
        for i in sig_idx:
            ax.text(fc[i], neglogp[i], gene_names[i], fontsize=5.5,
                    ha="center", va="bottom", clip_on=True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


def ma_plot(ax, mean_expr, log2fc, pval=None, fc_thresh=1.0, p_thresh=0.05,
            xlabel="mean normalized expression", ylabel="log2 fold change"):
    """MA plot: mean expression (x) vs log2 fold change (y)."""
    m = np.asarray(mean_expr, float)
    fc = np.asarray(log2fc, float)
    if pval is not None:
        up, down, ns = _threshold_mask(fc, pval, fc_thresh, p_thresh)
        ax.scatter(m[ns], fc[ns], s=6, c=SIGNIFICANT_SCHEME["ns"], alpha=0.5, linewidths=0)
        ax.scatter(m[down], fc[down], s=8, c=SIGNIFICANT_SCHEME["down"], alpha=0.8, linewidths=0)
        ax.scatter(m[up], fc[up], s=8, c=SIGNIFICANT_SCHEME["up"], alpha=0.8, linewidths=0)
    else:
        ax.scatter(m, fc, s=6, c=PALETTE["blue_main"], alpha=0.6, linewidths=0)
    ax.axhline(0, color="0.4", linewidth=0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


def dot_plot(ax, expression, genes, clusters, pct=None, cmap="viridis",
             size_range=(8, 60), vmin=None, vmax=None, xlabel=None, ylabel=None):
    """Single-cell marker dot plot: genes (y) x clusters (x).

    ``expression`` is a ``(n_genes, n_clusters)`` matrix (e.g. scaled mean
    expression) → dot **colour**. ``pct`` (optional, same shape) is the
    % expressed → dot **size**. If ``pct`` is None, size also scales with
    ``expression``.
    """
    m = np.asarray(expression, float)
    n_genes, n_clusters = m.shape
    size_src = np.asarray(pct, float) if pct is not None else m
    X, Y = np.meshgrid(np.arange(n_clusters), np.arange(n_genes))
    s_min, s_max = size_src.min() if size_src.size else 0, size_src.max() if size_src.size else 1
    size = (size_src - s_min) / (s_max - s_min) if s_max > s_min else np.zeros_like(size_src)
    size_px = size_range[0] + (size_range[1] - size_range[0]) * size
    sc = ax.scatter(X.ravel(), Y.ravel(), s=size_px.ravel(), c=m.ravel(),
                    cmap=cmap, vmin=vmin, vmax=vmax, linewidths=0.4, edgecolor="white")
    ax.set_xticks(np.arange(n_clusters))
    ax.set_xticklabels(clusters, rotation=40, ha="right")
    ax.set_yticks(np.arange(n_genes))
    ax.set_yticklabels(genes)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.figure.colorbar(sc, ax=ax, shrink=0.8, label="scaled expression")
    return ax


def umap_scatter(ax, x, y, labels, palette="tol_bright", size=14,
                 alpha=0.75, xlabel="UMAP-1", ylabel="UMAP-2"):
    """UMAP-style 2-D embedding coloured by cluster.

    ``labels``: per-point cluster id (length matches x/y). Points are coloured
    by cluster using a named colorblind-safe palette; a legend is drawn.
    """
    labels = np.asarray(labels)
    pal = friendly_pal(palette)
    uniq = list(dict.fromkeys(labels))
    for i, c in enumerate(uniq):
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
    parts = []
    for c in uniq:
        parts.append(data[groups == c])
    pal = friendly_pal(palette)
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
