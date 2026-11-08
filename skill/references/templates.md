# templates — quick patterns

Copy the style + pick a template. All in `examples/`.

## Bar (grouped, semantic colors)

```python
style()
fig, ax = plt.subplots(figsize=figsize["single"])
grouped_bar(ax, ["A","B"], [[0.9,0.8],[0.7,0.6]], ["Ours","Base"], ylabel="Score")
finish(ax); save(fig, "out/bars")
```

## Trend + CI

```python
trend(ax, x, [train_ms, valid_ms], ["Train","Valid"], ylabel="Acc")  # (N,2) = mean/std
```

## Multi-panel

```python
fig, axes = grid(2, 3, width="double")
# plot into each axes ; panel_letters(axes) ; finish each
```

## When to share axes

- share y: same quantity, same scale.
- don't share: different quantity (would squash one panel).
