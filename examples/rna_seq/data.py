#!/usr/bin/env python3
"""Synthetic RNA-seq read-count / QC data for a few samples.

Deterministic sample-level metrics (read count, genes detected, mapping rate) plus
counts for a handful of genes — enough for a QC + gene-expression figure.
"""
import numpy as np


def build(n_genes=800, seed=0):
    rng = np.random.default_rng(seed)
    samples = ["Con-1", "Con-2", "Trt-1", "Trt-2"]
    group = np.array(["control", "control", "treated", "treated"])
    # QC metrics per sample
    qc = {
        "reads": np.array([38, 41, 36, 43], dtype=float) * 1e6,
        "genes": np.array([16500, 17200, 15900, 17800], dtype=float),
        "map_rate": np.array([0.91, 0.93, 0.89, 0.94]),
    }
    # gene counts (genes x samples), negative-binomial-like (as float)
    base = rng.gamma(2.0, 500.0, n_genes)
    counts = np.array([rng.poisson(base * (1.0 if g == "control" else 0.15))
                       for g in group]).T.astype(float)
    counts[0] *= [1.0, 1.1, 3.0, 3.2]   # one strongly up-regulated gene
    return {"samples": samples, "group": group, "qc": qc,
            "counts": counts, "n_genes": n_genes}


if __name__ == "__main__":
    d = build()
    print(f"samples={d['samples']} genes={d['n_genes']}")
