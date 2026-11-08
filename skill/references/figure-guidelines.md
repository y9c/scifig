# figure-guidelines — how to make a figure

## Ask first (before any code)

1. claim — the one point?
2. venue + width — journal? single/half/double?
3. panels — how many, which share axes?
4. data — table, units, N, grouping?
5. chart type + thresholds — e.g. volcano `|log2FC|>1`, `padj<0.05`?

State your defaults; batch; restate the plan in one line.

## Do

1. Copy the style + helpers (`house-style.md`).
2. Find the closest recipe (`examples/`), copy + adapt.
3. Plot, then `ticks(ax)`, panel letter, save PDF.

## Check (before saying done)

- re-open the figure: no overlap, no clipping, letters clear, legend placed.
- vector PDF, correct final size.
