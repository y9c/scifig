# NOTICE / Attribution

This repository mixes two licensed sources. Read carefully before redistributing.

## What is MIT (this repo's LICENSE)

- `scifig/` — the Python package (style, palette, helpers, compose). Authored here.
- `examples/` — example scripts. Authored here.
- The `.mplstyle` files under `scifig/assets/` were derived from the personal
  `modern-matplotlib` / `scientific_publication` styles (originally local).

## What is CC BY-NC 4.0 (upstream, non-commercial)

- `skill/demos/figure_*` — reproducible scripts for published paper figures,
  vendored from [figures4papers](https://github.com/ChenLiu-1996/figures4papers),
  author **Chen Liu (刘晨)**, Yale University Computer Science PhD candidate.
- `skill/references/*` (methodology text: design-theory, common-patterns,
  tutorials, api, demos) also derive from that repo's `scientific-figure-making/`.

> **Correction to the earlier summary**: the original plan and the old NOTICE.md
> called figures4papers "MIT". The repo's actual `LICENSE` file is
> **CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International)**. This project's
> `LICENSE`/`NOTICE` reflect that corrected fact. Before any **commercial** use of
> the demos or the derived reference text, review the upstream license.

Papers represented by the vendored demos (citation per academic norms):

- **ImmunoStruct** — Nature Machine Intelligence 2026
- **LM-Dispersion** — ICML 2026
- **VIGIL** — ECCV 2026
- **RNAGenScape** — NeurIPS 2026 / arXiv 2025
- **Brainteaser** — NeurIPS 2025
- figure_CellSpliceNet / figure_ophthal_review / figure_Cflows

Full citations and paper links are in the upstream README:
https://github.com/ChenLiu-1996/figures4papers
