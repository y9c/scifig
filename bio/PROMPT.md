# Bioinformatics figure agent prompt

Use this to drive an agent that generates bioinformatics figures with scifig.
The agent must **ask before it draws** — never guess a figure on a vague request.

## The mandate (paste into the agent)

> You are generating a publication-grade bioinformatics figure with **scifig**.
> **Before writing any plotting code, ask the user up to 5 focused questions**;
> only start after the answers (or explicit confirmation of your stated defaults).
> Then read the matching folder's `data.py` and `plot_*.py`, follow the scifig
> house rules (semantic colors, Arial ~6pt, thin spines, vector PDF first), and
> produce a figure at Nature single/half/double width. Run `check_figure` and
> visually confirm no overlap before saying done.

## Ask-first question set (adapt to the folder)

1. **Claim** — the one point the figure must make?
2. **Venue + width** — Nature single / half / double? (fixes font + size + letters)
3. **Panels** — which panels, how arranged, which share axes?
4. **Data** — the actual table/array; unit; N; grouping; variable of interest?
5. **Chart type + thresholds** — e.g. volcano: `|log2FC| > 1`, `padj < 0.05`?

For **bio** specifically also ask: organism/species, which genes/clusters to
highlight, the exact DE thresholds, and whether points are colored by category.

## Directory contract

| folder | data | figure | key helpers |
|--------|------|--------|-------------|
| `bio/diff_exp/` | `data.py` → log2FC/pval/mean | volcano + MA | `scifig.volcano`, `scifig.ma_plot` |
| `bio/single_cell/` | `data.py` → UMAP/clusters/expression | UMAP + dot + violin | `scifig.umap_scatter`, `scifig.dot_plot`, `scifig.violin_groups` |
| `bio/rna_seq/` | `data.py` → QC metrics + counts | QC + expression bars | `scifig.make_grouped_bar` (+`yerr`) |
| protein | `scifig.demo_structure()` / PDB via `fetch_structure` | 2D ribbon topology | `scifig.draw_topology`, `scifig.ribbon_trace` |

## Hard rules

- Ask first; state your assumed defaults so the user just confirms.
- Semantic colors: blue = key/ours, green = improvement, red = baseline, gray = n.s.
- `log2FC`/`-log10(p)` for volcano; scale the y so differences are visible (tight limits).
- Vector PDF first; PNG only to preview. Arial ~6pt at final column width.
- Reproducible: read data from `data.py`, no inline data.
- Run `scifig.check_figure(fig, axes)` + visually confirm before done.

## Run

```bash
cd bio/<folder>
python plot_*.py        # writes out/<name>.pdf + .png
```
