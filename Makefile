# scifig — reproducible dev/plot env via uv
# Usage:  make setup | make run | make test | make mcp | make figs | make clean

UV      ?= uv
PY      ?= python
VENV    := .venv

.PHONY: setup run test mcp figs lint build release clean lock

setup:            ## create the env + install the package (dev + examples extras)
	$(UV) venv --python 3.11 $(VENV)
	$(UV) pip install --python $(VENV)/bin/python -e ".[dev,examples]"

run:              ## install and run all example scripts
	cd $(VENV)/bin && for e in ../examples/*.py; do $(PY) "$$e" || echo "FAIL: $$e"; done

test:             ## run any pytest tests (none yet) + import smoke
	$(UV) run --python $(VENV)/bin/python -c "import scifig; print('ok', scifig.__version__)"

figs:             ## regenerate all example figures (vector PDFs + preview PNGs)
	for e in examples/*.py; do $(UV) run --python $(VENV)/bin/python $$e || echo "FAIL: $$e"; done

build:            ## build the wheel + sdist
	$(UV) build

release: lint build   ## verify then build a distributable
	echo "Release artifacts in dist/. Publish with: git push -u origin main"

mcp:              ## start the MCP server (needs the mcp extra)
	$(UV) run --python $(VENV)/bin/python -m scifig.mcp_server

lint:             ## ruff lint
	$(UV) run --python $(VENV)/bin/python -m ruff check scifig

clean:            ## remove build artifacts / generated figures
	rm -rf build dist *.egg-info out .ruff_cache

lock:             ## regenerate uv.lock
	$(UV) lock --python 3.11
