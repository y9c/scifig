# Figure-generation contract (agent-first)

This is how an agent makes a scifig-style figure. There is no package: the agent
reads the house style + examples, then implements in the user's environment with
plain matplotlib. The agent is first-class — it asks, decides, implements,
verifies.

## Ask before you draw (mandatory)

Ask up to 5 focused questions before writing code. Never plot on a guess.

1. **Claim** — the one point this figure must make?
2. **Venue + width** — journal? single/half/double? (sets font + size + letters)
3. **Panels** — how many, how arranged, which share axes?
4. **Data** — the table/array, units, N, grouping, variable of interest?
5. **Chart type + thresholds** — e.g. volcano `|log2FC|>1`, `padj<0.05`?

Rules: infer (don't guess) what's unambiguous; batch questions; state your
default so the user just confirms; restate the plan in one line before coding.

## Decision ladder

1. **Check the capability map** ([capability-spec.md](capability-spec.md)) — find
the closest figure type; read its example.
2. **Copy the house style** ([house-style.md](house-style.md)) — paste the style
preamble + reusable helpers.
3. **Implement** the figure logic in plain matplotlib (adapt the closest example).
4. **Polish** (readable ticks, subtle grid or off, panel letter at corner, units).
5. **Verify** — re-open the saved figure, confirm no overlap/clipping, letters
clear, legend placed, vector PDF. Only then claim done.

## The universal pattern

```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
# 1) house style (paste from house-style.md)
# 2) figure at final physical size
fig, ax = plt.subplots(figsize=(3.5, 2.6))
# 3) any figure logic (adapt the closest example)
# 4) polish + panel letter
# 5) vector-first save
fig.savefig("out/fig.pdf", bbox_inches="standard")
```

## House rules (every figure)

- Arial ~5-6pt at final column width; lowercase Nature letters, uppercase bold Science.
- Semantic colors: blue=key, green=improve, red=baseline; never hardcode hex.
- Units + N + uncertainty on the figure.
- Vector-first: PDF primary; `pdf.fonttype=42`; `savefig.bbox=standard`.
- Reproducible: read data from a path; no inline data > ~20 rows.
- Verify: re-open the figure and confirm no overlap, no clipping, letters clear.

## Anti-patterns

- Default matplotlib colors / ticks / figure size.
- `bbox_inches="tight"` on the final export (changes size; use `standard`).
- Per-script rcParams patching — use the house-style preamble once.
- A legend overlapping data, or a colorbar label jammed into an axis label.

## Related

- [house-style.md](house-style.md) — the look (copy-paste)
- [capability-spec.md](capability-spec.md) — what's covered
- [api.md](api.md) — `_house` helper signatures
- [templates.md](templates.md) — figure-type templates
- [../examples/](../../examples/) — runnable recipes
