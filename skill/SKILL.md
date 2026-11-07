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

There is no package. Copy the house style (`references/house-style.md`), then
write the plot with plain matplotlib, adapting the closest example:

```python
# 1) paste the house-style preamble from references/house-style.md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
# 2) figure at final physical size
fig, ax = plt.subplots(figsize=(3.5, 2.6))
# 3) any figure logic (adapt the closest example in examples/)
ax.bar([0, 1], [0.9, 0.8], color="#0F4D92", edgecolor="black", linewidth=0.5)
ax.set_ylabel("Accuracy")
# 4) vector-first save
fig.savefig("out/fig.pdf", bbox_inches="standard")
```

Use the `_house` helpers (`grouped_bar`, `trend`, `heatmap`, `scatter`, `grid`,
`save`, `finish`, `panel_letters`, ...) for common shapes, and the recipes in
`examples/` (`biofigs.py`, `proteinfig.py`) for domain figures. The agent reads
the capability map and the closest recipe, then implements in the user's env.

## House rules

- **Arial ~5-6pt** at final column width; lowercase Nature letters, uppercase bold
  Science.
- **Semantic colors**: blue=key, green=improve, red=baseline.
- **Vector-first**: PDF default; `pdf.fonttype=42`; `savefig.bbox=standard`.
- **Readable/minor ticks, subtle grid or off**, thin spines, panel letters at
  the top-left corner.
- **Reproducible**: read data from a path; no inline data; no AI images.
- **Verify**: re-open the saved figure and confirm no overlap, no clipping,
  letters clear, legend placed before claiming done.

## References

| File | Open when |
|------|-----------|
| [references/house-style.md](references/house-style.md) | **FIRST** — the look: copy-paste rcParams + helpers + palette |
| [references/capability-spec.md](references/capability-spec.md) | what figure types are covered (capability map) |
| [references/figure-guidelines.md](references/figure-guidelines.md) | agent contract: ask-first, decision ladder, polish, verify |
| [references/templates.md](references/templates.md) | learn-by-example: universal rules + figure-type templates |
| [references/api.md](references/api.md) | `_house` helper signatures |
| [../examples/](../../examples/) | runnable recipes to read & adapt |

## License

MIT. See `LICENSE`.