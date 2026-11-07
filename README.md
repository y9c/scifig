# scifig

A **skill** for making publication-grade scientific figures. There is no package
to install. `scifig` gives an agent the conventions, a copy-paste house style,
and plain-matplotlib recipes, so it can implement any figure in the user's own
environment.

## What's here

| Path | What it is |
|------|-----------|
| `skill/` | the skill: house style, capability spec, agent workflow |
| `skill/references/house-style.md` | **copy-paste** rcParams + helpers (the look) |
| `skill/references/capability-spec.md` | what figure types are covered, and how |
| `examples/` | runnable plain-matplotlib recipes to read & adapt |

## Quick start (no install)

Read `skill/references/house-style.md` and paste the style preamble at the top of
your script; write the plot; save a vector PDF:

```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
# ...paste the house-style preamble from skill/references/house-style.md...
fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.bar([0, 1], [0.9, 0.8], color="#0F4D92", edgecolor="black", linewidth=0.5)
ax.set_ylabel("Accuracy")
fig.savefig("out/fig.pdf", bbox_inches="standard")   # vector
```

Or run an example: `python examples/grouped_bar.py` → `out/grouped_bar.pdf`.

## For an agent

Give the agent `skill/` (or this repo). It reads `capability-spec.md` (what's
covered), `house-style.md` (the look), and the `examples/` recipes, then
implements the figure with plain matplotlib in the user's environment. It
**asks first, then implements**, and verifies before claiming done.

## Conventions baked into the house style

Nature-style Arial ~5-6pt at final column width; semantic colors (blue=key,
green=improve, red=baseline); thin spines, no grid clutter; editable vector text
(`pdf.fonttype=42`); exact-size save (`savefig.bbox=standard`); panel letters at
the corner.

See `skill/SKILL.md` and `docs/` for details.
