# Real-World Demos and Figure Scripts

The design theory, patterns, and guidance in this skill are derived from the
figure-making scripts in the [figures4papers](https://github.com/ChenLiu-1996/figures4papers)
repository. This skill vendors a **script-only** copy of those canonical demos under
`demos/` (the generated `figures/*.png` outputs are intentionally not vendored to
keep the repo small). Those vendored scripts are the canonical reference for the
house style.

## Project folders (demos)

Each `demos/figure_*/` folder contains the Python scripts that were published in the
top-venue papers. Use them as references for bar charts, trend/line panels, heatmaps,
radar/polar comparisons, and multi-panel layouts.

| Project | Local scripts | Notes |
|--------|---------------|-------|
| **figure_ImmunoStruct** | `demos/figure_ImmunoStruct/` | Bar plots for quantitative comparison |
| **figure_CellSpliceNet** | `demos/figure_CellSpliceNet/` | Bar comparison, ablation |
| **figure_Brainteaser** | `demos/figure_Brainteaser/` | Bar composition breakdown |
| **figure_VIGIL** | `demos/figure_VIGIL/` | Radar plots, line plots |
| **figure_ophthal_review** | `demos/figure_ophthal_review/` | Trend plots |
| **figure_RNAGenScape** | `demos/figure_RNAGenScape/` | Heat maps |
| **figure_Dispersion** | `demos/figure_Dispersion/` | 3D-style spheres, performance plots |
| **figure_Cflows** | `demos/figure_Cflows/` | Comparison, ablation, trajectory plots |

For full scripts + generated outputs, clone or browse the upstream repo. The
`figure_*` scripts there are the canonical implementations of this house style
(the local `scifig` package re-implements the shared helpers those scripts used
to inline).

> Licensing note: these demos come from figures4papers (author **Chen Liu**, Yale),
> which is licensed **CC BY-NC 4.0** (non-commercial). See `NOTICE.md` in this
> repo for attribution and the distinction from the MIT license that covers the
> `scifig` package itself.

## Related files

- [SKILL.md](../SKILL.md) — when to use this skill
- [api.md](api.md) — the `scifig` package API
- [common-patterns.md](common-patterns.md) — layout and legend patterns
- [design-theory.md](design-theory.md) — style theory and reproduction rules
- [tutorials.md](tutorials.md) — step-by-step figure builds
- [cookbook.md](cookbook.md) — min-code recipes
