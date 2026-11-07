# scifig — no package to install. Just run the examples.
# Needs python3 with matplotlib + numpy + scipy. Uses .venv/bin/python if present,
# else system python3.

PY      ?= python3
ROOT    := $(shell pwd)
FALLBACK:= $(shell [ -x .venv/bin/python ] && echo $(ROOT)/.venv/bin/python || echo python3)

.PHONY: figs run venv

venv:             ## create a local env with the plotting deps
	uv venv --python 3.11 .venv
	uv pip install --python .venv/bin/python matplotlib numpy scipy

figs:             ## run every figure example; each writes out/<name>.pdf (+ .png preview)
	cd examples && for e in *.py; do \
		case $$e in _house.py|biofigs.py|proteinfig.py|pymol_render_aicda.py) continue;; esac; \
		echo "== $$e =="; $(FALLBACK) $$e || echo "FAIL: $$e"; \
	done
	cd examples && for d in diff_exp single_cell rna_seq; do \
		echo "== $$d =="; $(FALLBACK) $$d/plot_*.py || echo "FAIL: $$d"; \
	done

run: figs
