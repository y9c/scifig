# capability-spec — what's covered

Everything is a recipe in `examples/`. The agent picks the closest, copies it.

| Figure | Example |
|--------|---------|
| bars (+error) | `grouped_bar.py`, `benchmark_parity.py` |
| box / stacked / pie | `boxplot.py`, `stacked_bar.py`, `pie.py` |
| trend + CI | `trends_grid.py` |
| heatmap | `heatmap.py` |
| scatter / scatter+fit | `compose_annotate.py`, `scatter_fit.py` |
| ROC / confusion | `roc.py`, `confusion.py` |
| survival (KM) | `survival.py` |
| multi-panel benchmark | `benchmark_nature.py` |
| volcano / MA | `biofigs.py`, `single_cell/` |
| UMAP / dot / violin | `biofigs.py` |
| RNA-seq QC | `rna_seq/` |
| protein (PyMOL or vector) | `proteinfig.py`, `showcase_protein.py` |
| inset / compose panels | `showcase_inset.py`, `compose_annotate.py` |

New figure type? add an example + a row here. No package.
