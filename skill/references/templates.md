# Figure templates & universal rules

There are far more figure combinations than anyone should memorize. scifig's
point: **templates are few, rules are universal**, the details (spacing, colors,
letters, polish) are baked into the house style. Copy a template, swap data, done.

## Universal rules

| Rule | Detail |
|------|--------|
| **Semantic colors** | blue=key/your method, green=improvement, red/neutral=baseline. Never random hex. |
| **Arial 5-6pt** | at final column width; lowercase letters (Nature) or uppercase bold (Science). |
| **Thin spines** | top/right off; ~0.8pt. Interior grid subtle & behind data, or off. |
| **Readable ticks** | 4-6 major ticks + minor ticks. No matplotlib defaults. |
| **Units + N + uncertainty** | axis labels carry units; error bars / CI shown. |
| **Colorblind+grayscale** | distinct luminance; add marker/linestyle variety when overlapping. |
| **Vector-first** | PDF primary; `savefig.bbox='standard'`. PNG only to preview. |
| **No overlap/extra gap** | panel letters at the top-left corner; check spacing on the saved figure. |
| **One story** | each panel makes one defensible point; don't decorate. |

## Reference templates (use the `_house` helpers)

### Grouped bar (multi-series)

```python
from _house import style, grouped_bar, save
style()
fig, ax = plt.subplots(figsize=(3.5, 3.5))
grouped_bar(ax, ["VQA", "OCR"], [[0.92, 0.89], [0.83, 0.80]],
            ["Our method", "Baseline"], ylabel="Accuracy", ours_marker="Our method")
save(fig, "out/bars")   # -> out/bars.pdf
```

### Trend / training curve with confidence band

```python
from _house import trend
# ys entries are 1D or (N,2) mean/std -> draws a CI band
trend(ax, steps, [train_ms, valid_ms], ["Train", "Valid"],
      ylabel="Accuracy", xlabel="Epoch", ours_marker="Train")
```

### Heatmap

```python
from _house import heatmap
heatmap(ax, corr, x_labels=feats, y_labels=feats, cmap="RdBu_r", cbar_label="Pearson r")
```

### Scatter

```python
from _house import scatter
scatter(ax, latency, accuracy, label="Config", size=28)
```

### Multi-panel with shared legend

```python
from _house import grid, panel_letters, finish
fig, axes = grid(2, 3, width="double", aspect=0.5)
# ...plot into each axes...
panel_letters(axes, case="lower")
for a in axes: finish(a)
```

## When to share vs. not share axes

- **Share y** when panels compare the **same quantity on the same scale** —
  directly comparable.
- **Don't share** when quantities differ (accuracy vs. loss) — a shared y would
  squash one panel. Share only within same-quantity groups.

## Go deeper

- [house-style.md](house-style.md) — the look (copy-paste)
- [capability-spec.md](capability-spec.md) — what's covered
- [api.md](api.md) — `_house` signatures
- [figure-guidelines.md](figure-guidelines.md) — agent workflow
- [../../examples/](../../examples/) — runnable recipes
