#!/usr/bin/env python3
"""Protein topology figure — pure-vector cartoon, publication-ready.

Renders a protein Cα topology (helix ribbons + beta-sheet arrows) as a **vector**
matplotlib cartoon and labels key secondary-structure elements. Exports PDF/SVG
(no bitmap), so it can be inserted as a panel/inset of a larger figure without
losing vector quality.

No PyMOL needed. Load a real PDB via ``scifig.fetch_structure(pdb_id)`` (Biotite)
or use the built-in ``demo_structure``.
"""
import matplotlib
matplotlib.use("Agg")
import scifig

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.5, axes_linewidth=0.8))
fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("double", aspect=0.5))

# Use a real PDB if Biotite is available, else the deterministic demo.
coords = scifig.fetch_structure("1CRN")  # crambin (small, well-known)
if coords is None:
    coords = scifig.demo_structure()
    sse = "h" * 240 + "e" * 80
else:
    sse = None  # Biotite symbols; draw_topology accepts a struct array

scifig.draw_topology(ax, coords, sse=sse, color=scifig.PALETTE["blue_main"])

# annotate a couple of secondary-structure elements
if coords.shape[0] >= 300:
    ax.annotate("α-helix", xy=(1.2, 8.0), xytext=(2.0, 6.3),
                fontsize=6, color="0.3", arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("β-sheet", xy=(17.0, 10.6), xytext=(13.5, 12.4),
                fontsize=6, color="0.3", arrowprops=dict(arrowstyle="->", lw=0.6))

ax.set_title("Protein topology (vector)", pad=4)
scifig.finalize_figure(fig, "out/showcase_protein", formats=["pdf", "png"], dpi=600)
print("wrote out/showcase_protein.pdf/png (vector)")
