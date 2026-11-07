# AGENT.md — Working in scifig

Guidance for AI agents (and humans) editing, extending, or publishing this repo.

## What this project is

`scifig` is a thin, **agent-oriented** matplotlib harness for publication-grade
scientific figures. Philosophy: **style lives in the package; your code writes
only data.** The agent describes *what* the figure is; scifig renders it in the
unified house style.

## Package layout

| Module | Responsibility |
|--------|----------------|
| `scifig/style.py` | styles (`apply_publication_style`, `apply_modern_style`), `FigureStyle`, lifecycle (`create_subplots`, `finalize_figure`), Nature/journal presets |
| `scifig/palette.py` | `PALETTE`, `DEFAULT_COLORS`, `MODERN_COLORS`, `COLORBLIND_SAFE`, `FRIENDLY_PALS` |
| `scifig/semantics.py` | semantic role→color mapping (`SEMANTIC_ROLES`, `assign_colors`, `role_color`) |
| `scifig/helpers.py` | plot primitives (`make_grouped_bar`, `make_trend`, `make_heatmap`, `make_scatter`, `make_sphere_illustration`) |
| `scifig/compose.py` | panel composition + annotation (`panel_grid`, `join_axes`, `join_figures`, `add_panel_label`, `shared_legend`, `add_inset`, `add_sig`) |
| `scifig/spec.py` | **declarative** `FigureSpec` + `render_spec` (the agent-facing entry point) |
| `scifig/figure.py` | **object-oriented** builder: `Figure` + typed `BarPanel`/`TrendPanel`/`HeatmapPanel`/`ScatterPanel` |
| `scifig/archetypes.py` | callable figure templates (`timeseries_ci`, `sorted_bar`, `grouped_bar`, `scatter_fit`, `heatmap`, `tornado`, `confusion`) |
| `scifig/journals.py` | publisher spec table (`journal_style`, `journal_figsize`, `fig_size_mm`) |
| `scifig/quality.py` | acceptance gate (`check_figure`, `QUALITY_AXES`) |
| `scifig/polish.py` | editorial polish (`finish_axes`, `finish_figure`, `bar_value_labels`, `tight_ylim`) |
| `scifig/layout.py` | audit + auto-fix panel overlap / excessive whitespace (`audit_layout`, `fix_layout`) |
| `scifig/fonts.py` | font detection + cross-platform Arial fallback |
| `scifig/bio.py` | bioinformatics: `volcano`, `ma_plot`, `dot_plot`, `umap_scatter`, `violin_groups` |
| `scifig/protein.py` | pure-matplotlib 2-D protein topology (`draw_topology`, `ribbon_trace`) |
| `scifig/mcp_server.py` | optional MCP adapter (thin; needs the `mcp` SDK / Python >=3.10) |

## How an agent should drive scifig

> **Read `skill/references/figure-guidelines.md` first** — it is the agent-first
> figure-generation contract (questions, decision ladder, polish checklist, hard
> rules, template). This section is the short version.

1. **Ask the user** for the *claim* (one line), the target journal, and the
   column width (single/half/double) if publication-bound.
2. **Describe, don't hand-write.** Prefer `FigureSpec` + `render_spec`; fall
   back to archetypes, then raw helpers, only when the shape is unusual.
3. **Semantic colors, never hex in user code.** Use `assign_colors(...,
   ours_marker="...")` so blue=our method, green=improvement, red=baseline
   hold automatically.
4. **Vector-first + polish.** `finalize_figure`/`save` default to PDF; apply
   the polish checklist (bar edges, readable/minor ticks, subtle grid, tight
   y-limits, offset value labels).
5. **Run the quality gate** (`check_figure`) before claiming done — plus the four
   judgment axes.

## House rules (non-negotiable)

- **Arial ~5-6pt at final column width** for Nature; lowercase panel letters for
  Nature, uppercase bold for Science. `panel_case="lower"|"upper"`.
- **Reproducible**: scripts read data from a path; no inline data > ~20 rows; no
  AI-generated images.
- **Colorblind + grayscale safe**: use a named palette (`friendly_pal`) and pair
  colors with distinct markers/linestyles when series overlap in luminance.
- **Units + N + uncertainty on the figure** (axis labels carry units; CI/error
  bars shown).
- **Exact-size vector**: `savefig.bbox='standard'` (do not silently switch to
  `tight`, which changes saved size). `pdf.fonttype=42` for editable text.
- **One style, once**: call `apply_publication_style`/`journal_style` at the top;
  never hand-edit rcParams per script.

## Conventions

- All code, comments, docstrings, and docs are **English**.
- New capabilities go in the appropriate module + exported from `scifig/__init__.py`
  and added to `__all__`.
- Every new public function gets a docstring with a runnable `>>>` example where
  it helps.
- When adding a reusable figure shape, add it as an **archetype**, not a hardcoded
  example script.

## Editing workflow

- Read the relevant module before editing; follow existing patterns, don't create
  a second convention.
- After a change, run the affected example(s) and, for a visual, rasterize the
  PDF (`pdftoppm -png -r 200 file.pdf out`) and inspect it.
- Non-trivial changes get a smoke run producing a real figure.

## Testing / verification

- **Set up the env first**: follow [`docs/install-prompt.md`](docs/install-prompt.md)
  (uv-based; the agent-facing setup + smoke-test procedure).
- `examples/*.py` are the smoke tests — each must run and produce a figure.
- `python -m pytest` is not wired up; run examples directly and inspect output.
- For a figure change, always regenerate and *visually* confirm (output size,
  no overlap, panel letters clear, legend not colliding).

## Licensing

- **MIT** covers the whole repo (`scifig/` package, `examples/`, `bio/`, `skill/`).
- See `LICENSE`. Make sure vendored/bundled assets carry their own licences if
  added later.

## Publish checklist for GitHub

1. **Clean** built/generated artifacts: `rm -rf out dist .ruff_cache` (figures are
   regenerable; `out/`, `*.png/pdf`, `.ruff_cache`, `.venv` are gitignored).
2. **Sync version** in `scifig/__init__.py` (`__version__`) and `pyproject.toml`
   (`version`) — must match.
3. **Regenerate** `uv.lock` if deps changed (`make lock`).
4. **Verify** end-to-end: `make lint` (ruff clean), `make figs` (all examples
   produce a vector PDF), and a dry wheel build (`uv build`).
5. Confirm `requirements.txt` is gone (uv.lock + pyproject groups are the source
   of truth). Update `README.md`, `skill/SKILL.md`, `references/api.md`, and
   `references/templates.md` if APIs changed.
6. Commit **all** of: `LICENSE`, `AGENT.md`, `README.md`,
   `pyproject.toml`, `uv.lock`, `Makefile`, `docs/architecture.md`, `scifig/`,
   `skill/`, `examples/`.
7. Push to your remote: `git remote add origin <url> && git push -u origin main`.
