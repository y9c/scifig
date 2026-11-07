# scifig Architecture & Environment

How scifig is structured, how to set up a reproducible plotting environment on
any machine, and how the MCP backend fits in. Read this if you're setting up a
new computer or packaging the tool for others.

## The three-layer design

scifig is deliberately split so each layer is thin and independently reusable:

```
skill/             GUIDANCE layer (thin, markdown)
                   tells the agent when to use scifig + the conventions
scifig/mcp_server  INTERFACE layer (thin, optional MCP adapter)
                   exposes the engine as schema'd tools to any MCP client
scifig/            ENGINE layer (thick, the real implementation)
                   styles, helpers, spec, archetypes, polish, quality, layout
```

- **Why not just a skill?** A skill is static guidance; every client still needs
  the package, and there's no tool discovery/schema. Style decisions get
  re-decided per client.
- **Why not just MCP?** The aesthetic/judgment (Nature vs Science letters,
  semantic colors, avoiding overlap) is guidance, not just a call. MCP alone
  strips that out.
- **Why the split?** The engine is the single source of truth. Both the skill
  (for an agent in your repo) and the MCP adapter (for any external client) wrap
  the *same* engine — no duplicated logic, backward-compatible evolution.

## MCP backend (optional)

`scifig/mcp_server.py` exposes the engine as MCP tools: `render_spec`,
`assign_semantic_colors`, `list_palettes`, `quality_axes`. Any MCP-capable
client (Claude Desktop, Cursor, VS Code, a gateway, custom agent) connects and
calls them without installing scifig or re-implementing style.

```
pip install "scifig[mcp]"          # pulls the MCP SDK (needs Python >=3.10)
scifig-mcp                        # starts a stdio MCP server
```

or per-Makefile: `make mcp`.

> The MCP SDK (`mcp`/`fastmcp`) requires **Python >=3.10**. The engine itself
> works on 3.10+. On 3.9 the MCP server is unavailable but `scifig` still
> imports (the adapter imports `mcp` lazily and raises a clear error). The
> `MCP_TOOLS`/`SCHEMA` contract in the module remains usable as documentation.

## Reproducible environment (cross-machine)

Dependency management is pinned and reproducible so any machine builds the same
environment:

| File | Purpose |
|------|---------|
| `pyproject.toml` | package metadata + dependency **groups** (`examples`, `mcp`, `dev`) |
| `uv.lock` | pinned, resolved dependency graph (the reproducible source of truth) |
| `Makefile` | one-command orchestration (`setup`, `run`, `figs`, `mcp`, `lint`) |

### Quick start on a new machine

```bash
# 1) clone
# 2) build the env exactly as locked
make setup            # = uv venv --python 3.11 .venv && uv pip install -e ".[dev,examples]"
# 3) regenerate all figures with the locked env
make figs
# 4) start the MCP adapter
make mcp
```

`uv` is recommended (fast, cross-platform, one lockfile for Linux/macOS/Windows).
`pixi` also works (conda-based) if you need system libs. The `uv.lock` is
checked in so every machine — and CI — resolves identical versions.

### System prerequisites

- **Python 3.10+** (3.11 recommended).
- **Arial / Helvetica** sans font for the journal look. On macOS/Windows these
  ship with the OS. On Linux install `ttf-mscorefonts-installer` (Arial) or use
  the Open `Liberation Sans` metric-compatible substitute; scifig's font stack
  falls back to DejaVu Sans if none match.
- **LaTeX** only if you enable `use_tex=True` (scifig defaults to matplotlib
  mathtext, so LaTeX is optional).

## Version control + OS coordination

- `uv.lock` is committed; `out/`, `*.pdf`, `*.png`, `.venv` are gitignored
  (figures are regenerable — never commit raster/vector artifacts).
- The style always renders at the **physical size you pick** (`figsize` in
  inches); it does not depend on the display DPI or OS. Raster previews use
  `figure.dpi`/`savefig.dpi`; vector PDF/SVG are DPI-independent.
- The engine pins matplotlib behavior via rcParams set in code + bundled
  `.mplstyle`, so output is identical across OS once the fonts match.

## Why this makes the tool "strong and usable"

- An agent in **your** repo reads the `skill/` and calls the engine directly.
- An agent in **another** environment connects via MCP and calls the same
  tools — no install, just the tool schema.
- Both produce identical-quality output because they share one engine.
- You move machines by copying the repo (or `git clone`), running `make setup`
  and `make figs`, and you're plotting in the same style minutes later.
