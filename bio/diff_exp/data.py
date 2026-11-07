#!/usr/bin/env python3
"""Synthetic differential-expression dataset (control vs treated, n=2000 genes).

Generates a realistic log2-fold-change / p-value table the volcano and MA plots
consume. Deterministic (seeded) so figures reproduce exactly.
"""
import numpy as np


def build(n_genes=2000, seed=0):
    rng = np.random.default_rng(seed)
    # genes with a spread of true log2 fold changes
    log2fc = rng.normal(0, 1.1, n_genes)
    # a few strongly regulated genes
    log2fc[:80] += rng.choice([-3, 3], 80) * (0.5 + rng.random(80))
    # p-values correlated with effect size (stronger effect = more significant)
    pval = np.exp(-np.abs(log2fc) * (1.2 + rng.random(n_genes)))
    pval = np.clip(pval + rng.uniform(0, 0.2, n_genes), 1e-12, 1.0)
    # mean normalized expression for the MA plot (log-scale)
    mean_expr = 4.0 + 2.5 * rng.random(n_genes) + 0.4 * log2fc
    return {
        "gene": [f"GENE{i:04d}" for i in range(n_genes)],
        "log2fc": log2fc,
        "pval": pval,
        "mean_expr": mean_expr,
    }


if __name__ == "__main__":
    d = build()
    print(f"genes={len(d['gene'])}  sig up={sum((d['log2fc'] > 1) & (d['pval'] < .05))}  "
          f"sig down={sum((d['log2fc'] < -1) & (d['pval'] < .05))}")
