# Protein structure rendering for publication (vector)

**Bottom line:** don't use PyMOL for *publication* protein figures if you need
**vector** output — it renders to a **bitmap** (PNG / ray trace), so a PyMOL
render inserted in a paper is a raster image.

## Options (2025)

| Tool | Output | Vector | Notes |
|------|--------|--------|-------|
| **PyMOL / ChimeraX** | PNG/PNG 3D render | no | great for 3-D *viewing* + camera orientation; bitmap for output |
| **cellscape** (MIT) | SVG cartoon outlines | yes | Goodsell-style residue/chain outlines + depth shading; needs a camera matrix (often from PyMOL/Chimera) |
| **FlatProt** (2025, BMC) | 2D SVG projection | yes | standardised 2D representation; best for comparing many structures |
| **Biotite** (MIT) | parses PDB + SSE | partial | structure parsing, no full cartoon renderer out of the box |
| **scifig `protein.py`** | matplotlib vector | yes | self-contained pure-matplotlib 2D cartoon (helix ribbons + sheet arrows), no external tool; exports PDF/SVG |

## When to use what

- **Vector insert in a figure** → scifig `protein.py` (pure matplotlib, no dependency)
  or cellscape/FlatProt SVG. Never PyMOL (bitmap).
- **3D rotating view** → PyMOL/ChimeraX *only* to pick the camera; then a vector
  cartoon via the matrix, not the bitmap.
- **Comparing many structures** → FlatProt 2D representation.

## scifig usage

```python
import scifig
coords = scifig.demo_structure()            # or fetch_structure(pdb_id) / load_structure(path)
sse = "h" * 120 + "e" * 60                 # optional secondary-structure labels
fig, ax = scifig.create_subplots(1, 1)
scifig.draw_topology(ax, coords, sse=sse)   # pure-vector 2D cartoon
scifig.finalize_figure(fig, "out/protein")  # vector PDF
```

`draw_topology`/`ribbon_trace` draw directly on a matplotlib axes, so the cartoon
can also be placed as a **panel or inset** of a larger figure — all vector.
