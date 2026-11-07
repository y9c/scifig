# Protein structure rendering (vector vs raster)

## Can PyMOL export a vector image?

**No.** PyMOL's render path is a raster ray-tracer; `ray` makes
"high-resolution photos" (bitmap). This build rejects vector formats directly:

```
cmd.save('out.svg')   # -> Error: File format not supported for export
cmd.save('out.eps')   # -> Error: File format not supported for export
```

`png` (from `ray`) is the only image export. So a PyMOL render inserted in a
paper is a **raster** image.

## Vector-native options

| Tool | Output | Vector | Notes |
|------|--------|--------|-------|
| **PyMOL** | PNG 3D render | no | best-looking 3D view; bitmap only |
| **cellscape** (MIT) | SVG cartoon outlines | yes | Goodsell-style outlines + depth shading; needs a camera matrix |
| **FlatProt** (2025) | 2D SVG projection | yes | standardised 2D representation |
| **scifig `proteinfig.matplotlib_cartoon`** | matplotlib vector | yes | real PDB coords + real SSE; exports PDF/SVG |

## Recommendation

- **Best-looking** → PyMOL (`proteinfig.pymol_cartoon`, raster PNG). Use ≥600 dpi
  at final size if the journal allows PNG.
- **True vector / editable** → `proteinfig.matplotlib_cartoon` (pure matplotlib),
  or cellscape / FlatProt SVG.
- PyMOL for the **camera view only**, then a vector cartoon via the matrix.

## scifig example

```python
from proteinfig import pymol_cartoon, matplotlib_cartoon
pymol_cartoon("5JJ4", "out/aicda.png", chain="A")   # raster, best look
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
matplotlib_cartoon(ax, "1CRN")                       # vector
```

`matplotlib_cartoon` needs Biotite (optional) for PDB parsing + real SSE; it
falls back to a demo fold if Biotite/network is unavailable.
