#!/usr/bin/env python3
"""Synthetic single-cell dataset (n=800 cells, 4 clusters, marker genes).

Deterministic UMAP-like embedding + per-cluster marker expression (mean + %
 expressed) for dot / violin plots. Clusters are labeled cell types.
"""
import numpy as np


def build(n=800, seed=0):
    rng = np.random.default_rng(seed)
    clusters = ["T cell", "B cell", "Monocyte", "NK cell"]
    labels = np.repeat(clusters, n // 4)
    centers = np.array([[0, 0], [5, 2], [2, 5], [6, 6]])
    pts = [centers[i] + rng.normal(0, 0.7, (n // 4, 2)) for i in range(4)]
    umap = np.vstack(pts)

    markers = ["CD3D", "MS4A1", "LYZ", "NKG7"]
    # cell-level expression (genes x cells); each marker high in its cluster
    expr = np.zeros((len(markers), n))
    for i, c in enumerate(clusters):
        rows = np.where(labels == c)[0]
        for j in range(len(markers)):
            base = 4.0 if j == i else 0.3
            expr[j, rows] = base + rng.normal(0, 0.5, len(rows))
    expr = np.clip(expr, 0, None)

    # per-gene-per-cluster mean expression and % expressed (for dot plot)
    mean_by_cluster = np.zeros((len(markers), len(clusters)))
    pct_by_cluster = np.zeros((len(markers), len(clusters)))
    for j, g in enumerate(markers):
        for c, cl in enumerate(clusters):
            vals = expr[j, labels == cl]
            mean_by_cluster[j, c] = vals.mean()
            pct_by_cluster[j, c] = (vals > 0.5).mean() * 100

    return {"umap": umap, "labels": labels, "clusters": clusters,
            "markers": markers, "expr": expr,
            "mean_by_cluster": mean_by_cluster, "pct_by_cluster": pct_by_cluster}


if __name__ == "__main__":
    d = build()
    print(f"cells={len(d['labels'])} clusters={d['clusters']} markers={d['markers']}")
    print("mean_by_cluster shape:", d["mean_by_cluster"].shape)
