# Figure Templates & Universal Rules

There are far more possible figure combinations than anyone should memorize. The
point of scifig is that **the templates are few, the rules are universal**, and
the details (spacing, colors, letters, polish) are baked in. This page is what
you learn from and reference — copy a template, swap data, done.

## Universal rules (apply to EVERY figure, regardless of type)

These never change. scifig enforces most of them automatically.

| Rule | Detail |
|------|--------|
| **Semantic colors** | blue=your method, green=improvement, red/neutral=baseline. Use the semantic palette, never random hex. |
| **Arial 5-6pt** | at the final column width; lower-case letters (Nature) or upper bold (Science). |
| **Thin spines** | top/right off; ~0.8pt. Interior grid subtle & behind data, or off. |
| **Readable ticks** | 4-6 major ticks + minor ticks. No matplotlib defaults. |
| **Units + N + uncertainty** | axis labels carry units; error bars / CI shown. |
| **Colorblind+grayscale safe** | distinct luminance; add marker/linestyle variety when overlapping. |
| **Vector-first** | PDF primary; `savefig.bbox='standard'` (exact size). PNG only to preview. |
| **No overlap, no excess gap** | use `layout='auto'` — scifig measures and fixes. Panel letters at the top-left corner. |
| **One story** | each panel makes one defensible point; don't decorate. |

## Decision ladder (which API)

1. **`FigureSpec` / `render_spec`** — a whole figure from one dict (most common).
2. **OO `Figure` + typed `*Panel`** — same engine, object-oriented, chainable.
3. **Archetype** — one figure, one call (`timeseries_ci`, `sorted_bar`, ...).
4. **Raw helpers** — unusual shape; call `finish_axes` yourself.

## Reference templates by figure type

Each is a filled example showing the OO form (equivalent dict form is the same
fields in `FigureSpec(panels=[...])`).

### Grouped bar (multi-series)

```python
fig = Figure(width="single", aspect=1.0, ncols=1)
fig.add(BarPanel(
    categories=["VQA", "OCR", "Chart"],
    series=[[0.92, 0.89, 0.90], [0.83, 0.80, 0.84], [0.78, 0.76, 0.80]],
    labels=["Our method", "Baseline A", "Baseline B"],
    our_marker="Our method", ylabel="Accuracy",
))
fig.savefig("out/bars")   # -> out/bars.pdf
```

### Trend / training curve with confidence band

```python
fig.add(TrendPanel(
    x=steps, ys=[train_mean_std, valid_mean_std],
    labels=["Train", "Valid"], our_marker="Train",
    ylabel="Accuracy", xlabel="Epoch", show_shadow=True,
))
```

### Heatmap

```python
fig.add(HeatmapPanel(matrix=corr, x_labels=feats, y_labels=feats,
                     cmap="RdBu_r", cbar_label="Pearson r"))
```

### Scatter (+ optional inset / fit)

```python
fig.add(ScatterPanel(x=latency, y=accuracy, label="Config", size=28))
```

### Multi-panel figure, shared legend, some panels share y

```python
fig = Figure(width="double", aspect=0.4, ncols=3, shared_legend=True,
             share_groups=[[0, 1]])   # panels a,b share y; c independent
fig.add(BarPanel(...))                # a
fig.add(BarPanel(...))                # b (shares y with a)
fig.add(TrendPanel(...))              # c (independent scale)
fig.savefig("out/multi")
```

## When to share vs. not share axes

- **Share y** when panels compare the **same quantity on the same scale** (e.g.
  two datasets' accuracy) — makes them directly comparable.
- **Don't share** when quantities differ (accuracy vs. loss) — a shared y would
  squash one panel. Use `share_groups` to share only within same-quantity groups.

## Go deeper

- [figure-guidelines.md](figure-guidelines.md) — the agent-first generation contract
- [api.md](api.md) — exact signatures
- [design-theory.md](design-theory.md) — why the rules exist
- [demos/](../demos/) — real published figures to imitate
- [python code](../examples/spec_benchmark.py) & [OO example](../examples/oo_figure.py) — runnable
