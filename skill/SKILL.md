---
name: scifig
description: >-
  Publication-grade matplotlib scientific figures, agent-first: declarative spec
  and object-oriented builders, plot archetypes, semantic colors, editorial
  polish, and vector export. Use for formal figures in papers/slides/reports or
  bioinformatics. Not for interactive dashboards, publication-less EDA, or
  Illustrator-first infographics.
---

# scifig — publication-grade matplotlib figures

scifig is a **platform + standards + universal interface + capability spec**
for an agent to make publication figures, **not** a library that implements
every plot type. It guarantees the *look and conventions*; the agent supplies
the *figure logic* by reading the capability spec and the recipes in
`examples/`. Style lives in the platform; your code writes only data.

> **Read `references/capability-spec.md` first** — it maps what scifig provides
> (built-in) versus what's a recipe to read & adapt, plus the universal rules.

## Ask before you draw (mandatory)

**Ask up to 5 focused questions before writing code.** Never plot on a guess.

1. **Claim** — the one point this figure must make?
2. **Venue + width** — journal? single/half/double? (sets font + size + letters)
3. **Panels** — how many, how arranged, which share axes?
4. **Data** — the table/array, units, N, grouping, variable of interest?
5. **Chart type + thresholds** — e.g. volcano `|log2FC|>1`, `padj<0.05`?

Rules: infer (don't guess) what's unambiguous; batch questions; state your
default so the user just confirms; restate the plan in one line before coding.

## Build a figure

```python
import scifig
spec = scifig.FigureSpec(
    width="double", aspect=0.45, ncols=3, panel_case="lower",
    panels=[
        dict(type="bar", categories=[...], series=[[...]], labels=["Our method", "Base"],
             our_marker="Our method", ylabel="Score"),
        dict(type="trend", x=..., ys=[...], labels=["Our method", "Base"],
             our_marker="Our method", ylabel="Val acc", xlabel="Epoch"),
        dict(type="heatmap", matrix=..., cmap="RdBu_r", cbar_label="r"),
    ],
)
fig, axes = scifig.render_spec(spec, "out/fig")   # -> out/fig.pdf
```

Or object-oriented (`Figure` + `BarPanel`/`TrendPanel`/`HeatmapPanel`/`ScatterPanel`)
or an archetype (one call: `volcano`, `timeseries_ci`, `sorted_bar`, ...).

## House rules

- **Arial ~5-6pt** at final column width; lowercase Nature letters, uppercase bold
  Science.
- **Semantic colors**: `assign_colors(labels, ours_marker=...)` — blue=ours,
  green=improve, red=baseline.
- **Vector-first**: PDF default; `pdf.fonttype=42`; `savefig.bbox=standard`.
- **Readable/minor ticks, subtle grid or off**, thin spines, panel letters at
  the top-left corner.
- **Reproducible**: read data from a path; no inline data; no AI images.
- **Run `check_figure`** (no FAIL) and visually confirm before done.

## References

| File | Open when |
|------|-----------|
| [references/capability-spec.md](references/capability-spec.md) | **FIRST** — what scifig provides, the capability map (built-in vs recipe), universal rules |
| [references/figure-guidelines.md](references/figure-guidelines.md) | agent contract: ask-first, decision ladder, polish, template |
| [references/templates.md](references/templates.md) | learn-by-example: universal rules + figure-type templates |
| [references/api.md](references/api.md) | exact function signatures |
| [../examples/](../../examples/) | runnable recipes to read & adapt |

## License

MIT. See `LICENSE`.