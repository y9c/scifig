# AGENT.md — working in scifig (a skill repo)

scifig is a **skill**, not a package. There is nothing to install. It gives an
agent the conventions (house style), a capability map, and plain-matplotlib
recipes (`examples/`). Keep it light — adding a feature means adding an example
or a doc, never a package.

## What's here

| Path | Purpose |
|------|---------|
| `skill/SKILL.md` | the skill: positioning, ask-first, house rules |
| `skill/references/house-style.md` | the look: copy-paste rcParams + helpers + palette |
| `skill/references/capability-spec.md` | what figure types are covered (map) |
| `skill/references/templates.md` | learn-by-example templates |
| `skill/references/api.md` | `_house` helper signatures |
| `skill/references/figure-guidelines.md` | agent workflow (ask-first, verify) |
| `examples/` | runnable plain-matplotlib recipes |
| `examples/_house.py` | the reusable house-style helpers (shared by examples) |

## Conventions

- All code, comments, docstrings, docs are **English**.
- Examples use **plain matplotlib** + `_house` (never a scifig package).
- Adding a figure type = add an example + a row in `capability-spec.md`. No package.
- Keep docs concise; no fluff.

## Editing workflow

- Read the relevant doc/example before editing; follow existing patterns.
- After a change, run the affected example(s) and inspect the saved PDF visually.
- New examples must run standalone from `examples/` (only matplotlib/numpy/scipy).

## Making or editing an example

- Start by copying the house-style preamble (`skill/references/house-style.md`).
- Use `_house` helpers for common shapes; add a new helper to `_house.py` only
  when it's genuinely reused.
- Save vector-first (PDF); `savefig.bbox="standard"`.
- Verify: re-open the saved figure — no overlap, no clipping, letters clear.

## Verification

- `make figs` runs every example in `examples/`; each must write `out/<name>.pdf`.
- Lint is not enforced (no ruff for a skill); rely on running the examples.
- For a figure change, always regenerate and visually confirm.

## License

MIT. See `LICENSE`.
