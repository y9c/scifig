"""MCP server exposing scifig as discoverable tools.

This makes scifig a **first-class, agent-agnostic tool**: any MCP-capable client
(Claude Desktop, Cursor, VS Code, custom agents) connects and calls
``render_spec``, ``check_figure``, ``list_palettes``, etc. via schema'd tools,
without each client installing scifig or reimplementing style conventions.

**Architecture:** the engine (this package) is the single source of truth; this
module is a thin adapter. Do not duplicate style / colour / layout logic here.

## Usage

The official MCP SDK is required to run the server: ``pip install mcp``. When
absent, this module still exposes :data:`MCP_TOOLS` — a plain description of the
tool schema — so an agent can be taught the interface (e.g. via the skill)
without the SDK.

    python -m scifig.mcp_server            # serves stdio by default
"""

from __future__ import annotations

from .palette import FRIENDLY_PALS, PALETTE
from .quality import QUALITY_AXES
from .semantics import assign_colors
from .spec import FigureSpec, render_spec

__all__ = ["MCP_TOOLS", "run_server", "SCHEMA"]

# Skill-facing contract: the tool names + a short description. The adapter turns
# these into @mcp.tool functions; used when the SDK is unavailable.
MCP_TOOLS = [
    {
        "name": "render_spec",
        "description": "Render a publication figure from a declarative FigureSpec "
        "dict (panels/width/aspect/panel_case/ours_marker/...). "
        "Returns the vector PDF path + a quality-gate verdict.",
    },
    {
        "name": "assign_semantic_colors",
        "description": "Assign semantic colors (blue=ours, green=improve, "
        "red=baseline) to a list of labels.",
    },
    {
        "name": "list_palettes",
        "description": "List colorblind-safe named palettes and the semantic PALETTE roles.",
    },
    {
        "name": "quality_axes",
        "description": "Return the four judgment axes (Depth/Elegance/"
        "Unimpeachable/Visible gap) for a figure review.",
    },
]

SCHEMA = {
    "render_spec": {
        "panels": {"type": "array", "items": {"type": "object"}},
        "width": {
            "type": "string",
            "enum": ["single", "half", "double", "full"],
            "default": "double",
        },
        "aspect": {"type": "number", "default": 0.4},
        "panel_case": {"type": "string", "enum": ["lower", "upper"], "default": "lower"},
        "ours_marker": {"type": "string", "default": None},
    },
    "assign_semantic_colors": {
        "labels": {"type": "array", "items": {"type": "string"}},
        "ours_marker": {"type": "string", "default": None},
    },
}


def _render_spec(
    panels, width="double", aspect=0.4, panel_case="lower", ours_marker=None, out="out/figure"
):
    spec = FigureSpec(
        panels=panels, width=width, aspect=aspect, panel_case=panel_case, layout="auto"
    )
    if ours_marker:
        for p in spec.panels:
            p.setdefault("ours_marker", ours_marker)
    fig, axes = render_spec(spec, out, formats=["pdf"], dpi=600)
    return {"figure": f"{out}.pdf", "panels": len(axes)}


def _assign_color(colors: list[str], ours_marker=None):
    return assign_colors(colors, ours_marker=ours_marker)


def run_server(transport: str = "stdio"):
    """Start the MCP server (requires the ``mcp`` SDK).

    Imported lazily so the package works without it. Raises a clear error if the
    SDK is missing (the :data:`MCP_TOOLS` / :data:`SCHEMA` contract still works).
    """
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - env dependent
        raise RuntimeError(
            "The 'mcp' SDK is required to run the scifig MCP server: "
            "pip install mcp. (The package and skill work without it.)"
        ) from exc

    mcp = FastMCP("scifig")

    @mcp.tool()
    def render_spec(
        panels: list[dict],
        width: str = "double",
        aspect: float = 0.4,
        panel_case: str = "lower",
        ours_marker: str = None,
        out: str = "out/figure",
    ) -> dict:
        """Render a publication figure from a declarative spec; returns the PDF path."""
        return _render_spec(panels, width, aspect, panel_case, ours_marker, out)

    @mcp.tool()
    def assign_semantic_colors(labels: list[str], ours_marker: str = None) -> dict:
        """Assign semantic colors to a list of series labels."""
        return {"colors": assign_colors(labels, ours_marker=ours_marker)}

    @mcp.tool()
    def list_palettes() -> dict:
        """List colorblind-safe named palettes and semantic palette roles."""
        return {"friendly": list(FRIENDLY_PALS), "semantic_roles": list(PALETTE)}

    @mcp.tool()
    def quality_axes() -> dict:
        """Return the four figure-review judgment axes."""
        return {"axes": QUALITY_AXES}

    mcp.run(transport=transport)
    return mcp


if __name__ == "__main__":
    run_server()
