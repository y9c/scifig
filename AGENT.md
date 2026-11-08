# AGENT.md — working in scifig

A skill repo. No package, no install. Adding a feature = add an example + a doc row.

## Conventions

- English.
- Examples: plain matplotlib + `examples/_house.py` (never a package).
- New figure type = add `examples/<name>.py` + a row in `skill/references/capability-spec.md`.
- Keep docs short and copy-ready.

## Edit flow

1. Read the closest example + `house-style.md`.
2. Write/adapt, then run it.
3. Check the saved figure: no overlap, letters clear, vector PDF.

## Verify

```bash
make figs   # runs all examples; each writes out/<name>.pdf
```

## License

MIT.
