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
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scifig
from proteinfig import matplotlib_cartoon

scifig.apply_publication_style(scifig.FigureStyle(font_size=6.5, axes_linewidth=0.8))
fig, ax = scifig.create_subplots(1, 1, figsize=scifig.nature_figsize("double", aspect=0.5))

# vector cartoon from a real PDB (Biotite), else demo fallback
matplotlib_cartoon(ax, "1CRN", color=scifig.PALETTE["blue_main"])

ax.set_title("Protein topology (vector)", pad=4)
scifig.finalize_figure(fig, "out/showcase_protein", formats=["pdf", "png"], dpi=600)
print("wrote out/showcase_protein.pdf/png (vector)")
