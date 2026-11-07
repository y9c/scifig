# Absorbed upstream sources (research notes)

scifig's agent-oriented core was built by studying the following repositories
and merging their strongest patterns. Keep this as provenance; each entry notes
what was absorbed.

## Syntax / reference packages

| Repo | What was absorbed |
|------|-------------------|
| **[figures4papers](https://github.com/ChenLiu-1996/figures4papers)** (Chen Liu, Yale; CC BY-NC 4.0) | house methodology; demos; semantic blue/green/red palette |
| **[SciencePlots](https://github.com/garrettj403/SciencePlots)** (garrettj403; MIT) | journal-style modular mplstyle; minimal spines; `savefig.bbox: tight` discipline |
| **[pypubfigs](https://github.com/JLSteenwyk/pypubfigs)** | colorblind-safe named palettes (Okabe-Ito / Tol / Wong / IBM / Tableau) → `FRIENDLY_PALS`, `friendly_pal` |
| **[scientific-plotting-conventions](https://github.com/jiutongzhao/scientific-plotting-conventions)** | publisher-safe defaults: `pdf.fonttype=42` editable TrueType, `savefig.bbox=standard` (exact size), size-patch stacking, `figure.figsize` in physical units |
| **[Icarus-Figures](https://github.com/TAO-QKV/Icarus-Figures)** | **callable archetypes (A1–A13)**, publisher journal-spec table (nature/science/cell/ieee/pnas/acs/rsc/elsevier/aps), quality bar + critique gate, reproducible/3-format-vector hard rules |
| **[cnsplots](https://github.com/faridrashidi/cnsplots)** | Cell/Nature/Science orientation; biomedical archetypes (survival, ROC); per-journal styling |
| **[scientific-agent-skills / scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills)** | publication-guideline checklist: units, N, uncertainty, error bars, significance, colorblind-safe |
| **[figure-hygiene](https://github.com/fkguo/nullius)** | correctness/legibility checklist for data figures |
| **[figure-review](https://github.com/skymanbp/sci-paper)** | read-every-actual-figure review discipline; trace scientific content |

## Patterns merged into scifig

1. **Journal presets** (`journals.py`): per-publisher single-column width + base
   font → `journal_style(name)`, `journal_figsize(name)`, `fig_size_mm(width_mm)`.
2. **Callable archetypes** (`archetypes.py`): `timeseries_ci`, `sorted_bar`,
   `grouped_bar`, `scatter_fit`, `heatmap`, `tornado`, `confusion` — pick a
   template, fill data, get a styled figure.
3. **Declarative spec** (`spec.py`): `FigureSpec` + `render_spec` — describe the
   figure, scifig enforces house style (semantic colors, shared legend, panel
   letters, vector PDF).
4. **Semantic colors** (`semantics.py`): `assign_colors(labels, ours_marker=...)`
   assigns role colors (blue=ours, green=improve, red=baseline) automatically.
5. **Colorblind-safe palettes** (`palette.py`): `FRIENDLY_PALS` + `friendly_pal`.
6. **Vector-safe defaults** (`style.py`): `pdf.fonttype=42`, `svg.fonttype=none`,
   `savefig.bbox=standard` (exact size), `legend.labelcolor=linecolor`.
7. **Quality gate** (`quality.py`): `check_figure` mechanical FAIL/OK + the four
   judgment axes (Depth · Elegance · Unimpeachable · Visible gap).

## Licensing note

All upstream code is referenced for *pattern* reuse. No upstream source file is
copied verbatim; scifig is a clean re-implementation. figures4papers demos/text
vendored in `skill/demos` and `skill/references` remain under their upstream
**CC BY-NC 4.0** license (see NOTICE.md) — not under scifig's MIT.
