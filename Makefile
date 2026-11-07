# scifig — no package to install. Just run the examples.
# Requires python3 with matplotlib + numpy + scipy (standard scientific Python).

PY      ?= python3

.PHONY: figs run

figs:             ## run every example; each writes out/<name>.pdf (+ .png preview)
	cd examples && for e in *.py; do \
		echo "== $$e =="; $(PY) $$e || echo "FAIL: $$e"; \
	done

run: figs
