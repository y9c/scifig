#!/usr/bin/env python3
"""Render AID (AICDA) as a clean, publication-grade PyMOL cartoon.

Single chain (chain A), white background, secondary-structure colouring, proper
lighting, high-res ray trace. This is the look expected in top journals — not a
multi-chain jumble.
"""
import pymol
from pymol import cmd

cmd.reinitialize()
cmd.load("data_5JJ4.pdb", "aicda")

cmd.remove("solvent")
cmd.remove("not polymer")

# isolate one chain (AID domain; A is a good representative), del the rest
cmd.select("one", "chain A")
cmd.remove("not one")
cmd.delete("one")

cmd.hide("everything")
cmd.show("cartoon", "polymer")
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_side_chain_helper", 1)

# secondary-structure colouring: helix blue, sheet red-orange, loop white/grey
cmd.color("white", "polymer")
cmd.color("marine", "ss H")   # alpha-helix
cmd.color("orange", "ss S")   # beta-sheet

cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)   # <- white background survives ray tracing
cmd.set("ray_trace_mode", 1)
cmd.set("ray_shadows", 0)             # cleaner, flat lighting for print
cmd.set("antialias", 2)
cmd.set("ambient", 0.5)
cmd.set("specular", 0.2)

cmd.orient()
cmd.zoom("polymer", 2.0)

cmd.ray(2200, 1800)
cmd.png("out/aicda_pymol.png", dpi=300)
print("wrote out/aicda_pymol.png (single chain, white bg, secondary-structure colors)")
