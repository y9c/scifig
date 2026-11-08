# api — the `_house` helpers

The reusable interface is `examples/_house.py`. Copy the pieces you need.

## Style + save

```python
from _house import style, figsize, save, finish, panel_letters, palette_labels
style()                                    # apply house look
fig, ax = plt.subplots(figsize=figsize("single"))
save(fig, "out/x")                        # -> out/x.pdf (vector)
```

## Plot builders

| Builder | What it does |
|---------|--------------|
| `grouped_bar(ax, cat, series, labels, **kw)` | grouped bars (+ `yerr`, `annotate`) |
| `trend(ax, x, ys, labels, **kw)` | lines + CI (2-col mean/std) |
| `heatmap(ax, matrix, **kw)` | heatmap + colorbar |
| `scatter(ax, x, y, **kw)` | scatter |
| `scatter_fit(ax, x, y, **kw)` | scatter + regression + CI |
| `boxplot(ax, data, labels, **kw)` | per-group box |
| `stacked_bar(ax, cat, parts, labels, **kw)` | composition |
| `pie(ax, values, labels, **kw)` | donut |
| `roc_curve(ax, y_true, y_score, **kw)` | ROC + AUC |
| `confusion(ax, cm, labels, **kw)` | annotated matrix |
| `grid(nr, nc, **kw)` | multi-panel → `(fig, axes)` |

## Polish

```python
finish(ax)                 # labels + readable ticks (keeps categorical x)
panel_letters(axes)        # a, b, c ...
bar_labels(ax, bars)       # value labels above bars
add_sig(ax, x0, x1, y)     # significance bracket
add_inset(ax, loc, size)   # inset axes
```

See `examples/_house.py` for signatures.
