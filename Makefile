PACKAGE         := lenstest
GITHUB_USER     := scottprahl

UV              ?= uv
RUN             := $(UV) run --extra dev
RUN_DOCS        := $(UV) run --extra docs
RUN_LITE        := $(UV) run --extra lite

RM              ?= rm -f
RMR             ?= rm -rf

ROOT            := $(abspath .)
DOCS_DIR        := $(ROOT)/docs
HTML_DIR        := $(DOCS_DIR)/_build/html
OUT_ROOT        := $(ROOT)/_site
OUT_DIR         := $(OUT_ROOT)/$(PACKAGE)
STAGE_DIR       := $(ROOT)/.lite_src
DOIT_DB         := $(ROOT)/.jupyterlite.doit.db
LITE_CONFIG     := $(ROOT)/$(PACKAGE)/jupyter_lite_config.json

# --- GitHub Pages deploy config ---
PAGES_BRANCH    := gh-pages
WORKTREE        := .gh-pages
REMOTE          := origin

# --- server config (override on CLI if needed) ---
HOST            ?= 127.0.0.1
PORT            ?= 8000

PYTEST_OPTS     :=
SPHINX_OPTS     := -T -E -b html -d $(DOCS_DIR)/_build/doctrees -D language=en

TEST_TARGETS                := tests/test_foucault.py tests/test_lenstest.py tests/test_ronchi.py
NOTEBOOK_TEST_TARGETS       := tests/test_all_notebooks.py
PYLINT_TARGETS              := $(PACKAGE)/*.py tests/*.py .github/scripts/update_citation.py
YAML_TARGETS                := .github/workflows/citation.yaml .github/workflows/pypi.yaml .github/workflows/test.yaml .readthedocs.yaml
RST_TARGETS                 := README.rst CHANGELOG.rst $(DOCS_DIR)/index.rst $(DOCS_DIR)/changelog.rst
RST_AUTOMODAPI_TARGETS      := $(DOCS_DIR)/$(PACKAGE).rst
DOC_NOTEBOOK_TARGETS        := $(DOCS_DIR)/*.ipynb
CLEAN_DIR_TARGETS           := .ruff_cache $(PACKAGE).egg-info $(DOCS_DIR)/api $(DOCS_DIR)/_build tests/charts dist
LITE_CLEAN_DIR_TARGETS      := $(STAGE_DIR) $(OUT_ROOT) $(DOIT_DB) .doit.db .jupyterlite.doit.db.db _output _site
REALCLEAN_DIR_TARGETS       := .cache .tmp $(WORKTREE) .venv $(DOCS_DIR)/api $(DOCS_DIR)/_static $(DOCS_DIR)/_templates

.PHONY: help
help:
	@echo "Build Targets:"
	@echo "  dist           - Build sdist+wheel locally"
	@echo "  html           - Build Sphinx HTML documentation"
	@echo "  lab            - Start jupyterlab"
	@echo "  readme         - Generate images used in README.rst"
	@echo "  venv           - Sync .venv with project dependencies"
	@echo ""
	@echo "Test Targets:"
	@echo "  test           - Run pytest on python files"
	@echo "  note-test      - Test all notebooks for errors"
	@echo ""
	@echo "Packaging Targets:"
	@echo "  rcheck         - Distribution release checks"
	@echo "  manifest-check - Validate MANIFEST"
	@echo "  pylint-check   - Lint python targets"
	@echo "  pyroma-check   - Validate overall packaging"
	@echo "  rst-check      - Validate all RST files"
	@echo "  ruff-check     - Lint all .py and .ipynb files"
	@echo "  yaml-check     - Validate YAML files"
	@echo ""
	@echo "JupyterLite Targets:"
	@echo "  lite           - Build JupyterLite site into $(OUT_DIR)"
	@echo "  lite-serve     - Serve $(OUT_DIR) at http://$(HOST):$(PORT)"
	@echo "  lite-deploy    - Upload to github"
	@echo ""
	@echo "Clean Targets:"
	@echo "  clean          - Remove build caches and docs output"
	@echo "  lite-clean     - Remove JupyterLite outputs"
	@echo "  realclean      - clean + remove .venv"

.PHONY: venv
venv:
	@echo "==> Syncing .venv with uv"
	@$(UV) sync --python $(PY_VERSION) --extra dev --extra docs --extra lite

.PHONY: dist
dist:
	$(RUN) python -m build

.PHONY: test
test:
	$(RUN) pytest $(PYTEST_OPTS) $(TEST_TARGETS)

.PHONY: note-test
note-test:
	$(RUN) pytest --verbose $(NOTEBOOK_TEST_TARGETS)
	@echo "✅ Notebook check complete"

.PHONY: html
html:
	@mkdir -p "$(HTML_DIR)"
	$(RUN_DOCS) sphinx-build $(SPHINX_OPTS) "$(DOCS_DIR)" "$(HTML_DIR)"
	@command -v open >/dev/null 2>&1 && open "$(HTML_DIR)/index.html" || true

.PHONY: yaml-check
yaml-check:
	@$(RUN) yamllint $(YAML_TARGETS)

.PHONY: rst-check
rst-check:    ## Validate all RST files
	@$(RUN) rstcheck $(RST_TARGETS)
	@$(RUN) rstcheck --ignore-directives automodapi $(RST_AUTOMODAPI_TARGETS)

.PHONY: pylint-check
pylint-check:
	@$(RUN) pylint $(PYLINT_TARGETS)

.PHONY: ruff-check
ruff-check:
	$(RUN) ruff check

.PHONY: manifest-check
manifest-check:
	$(RUN) check-manifest

.PHONY: pyroma-check
pyroma-check:
	$(RUN) pyroma -d .

.PHONY: rcheck
rcheck:
	@echo "Running all release checks..."
	@$(MAKE) realclean
	@$(MAKE) ruff-check
	@$(MAKE) pylint-check
	@$(MAKE) yaml-check
	@$(MAKE) rst-check
	@$(MAKE) manifest-check
	@$(MAKE) pyroma-check
	@$(MAKE) html
	@$(MAKE) lite
	@$(MAKE) dist
	@$(MAKE) test
	@$(MAKE) note-test
	@echo "✅ Release checks complete"

.PHONY: readme
readme:
	@cd $(DOCS_DIR) && $(RUN) python make_readme_images.py

.PHONY: lab
lab:
	@echo "==> Launching JupyterLab with uv-managed environment"
	$(RUN) python -m jupyter lab --ServerApp.root_dir="$(CURDIR)"

.PHONY: lite
lite: $(LITE_CONFIG)
	@echo "==> Building package wheel for PyOdide"
	@$(RUN) python -m build

	@echo "==> Checking for .gh-pages worktree"
	@if [ -d "$(WORKTREE)" ]; then \
		echo "    Found .gh-pages worktree, removing..."; \
		git worktree remove "$(WORKTREE)" --force 2>/dev/null || true; \
		git worktree prune; \
		$(RMR) "$(WORKTREE)"; \
		echo "    ✓ Removed"; \
	else \
		echo "    No .gh-pages worktree found"; \
	fi

	@echo "==> Cleaning previous builds"
	@$(RMR) "$(OUT_ROOT)"
	@$(RMR) "$(DOIT_DB)"
	@$(RMR) ".doit.db"
	@$(RMR) ".jupyterlite.doit.db.db"
	@echo "    ✓ Cleaned"

	@echo "==> Staging notebooks from docs -> $(STAGE_DIR)"
	@$(RMR) "$(STAGE_DIR)"; mkdir -p "$(STAGE_DIR)"
	cp $(DOC_NOTEBOOK_TARGETS) "$(STAGE_DIR)"
	@echo "==> Clearing outputs from staged notebooks"
	$(RUN) python -m jupyter nbconvert --clear-output --inplace "$(STAGE_DIR)"/*.ipynb
	@echo "==> Building JupyterLite"
	@$(RUN_LITE) jupyter lite build \
		--config="$(LITE_CONFIG)" \
		--contents="$(STAGE_DIR)" \
		--output-dir="$(OUT_DIR)"

	@echo "==> Adding .nojekyll for GitHub Pages"
	@touch "$(OUT_DIR)/.nojekyll"

	@echo "✅ Build complete -> $(OUT_DIR)"

.PHONY: lite-serve
lite-serve:
	@test -d "$(OUT_DIR)" || { echo "❌ run 'make lite' first"; exit 1; }
	@echo "Serving at"
	@echo "   http://$(HOST):$(PORT)/$(PACKAGE)/?disableCache=1"
	@echo ""
	$(RUN_LITE) python -m http.server -d "$(OUT_ROOT)" --bind $(HOST) $(PORT)

.PHONY: lite-deploy
lite-deploy:
	@echo "==> Sanity check"
	@test -d "$(OUT_DIR)" || { echo "❌ Run 'make lite' first"; exit 1; }

	@echo "==> Ensure $(PAGES_BRANCH) branch exists"
	@if ! git show-ref --verify --quiet refs/heads/$(PAGES_BRANCH); then \
	  CURRENT=$$(git branch --show-current); \
	  git switch --orphan $(PAGES_BRANCH); \
	  git commit --allow-empty -m "Initialize $(PAGES_BRANCH)"; \
	  git switch $$CURRENT; \
	fi

	@echo "==> Setup deployment worktree"
	@git worktree remove "$(WORKTREE)" --force 2>/dev/null || true
	@git worktree prune || true
	@$(RMR) "$(WORKTREE)"
	@git worktree add "$(WORKTREE)" "$(PAGES_BRANCH)"
	@git -C "$(WORKTREE)" pull "$(REMOTE)" "$(PAGES_BRANCH)" 2>/dev/null || true

	@echo "==> Deploy $(OUT_DIR) -> $(WORKTREE)"
	@rsync -a --delete --exclude ".git*" "$(OUT_DIR)/" "$(WORKTREE)/"
	@touch "$(WORKTREE)/.nojekyll"
	@date -u +"%Y-%m-%d %H:%M:%S UTC" > "$(WORKTREE)/.pages-ping"

	@echo "==> Commit & push"
	@cd "$(WORKTREE)" && \
	  git add -A && \
	  if git diff --quiet --cached; then \
	    echo "✅ No changes to deploy"; \
	  else \
	    git commit -m "Deploy $$(date -u +'%Y-%m-%d %H:%M:%S UTC')" && \
	    git push "$(REMOTE)" "$(PAGES_BRANCH)" && \
	    echo "✅ Deployed to https://$(GITHUB_USER).github.io/$(PACKAGE)/"; \
	  fi

.PHONY: clean
clean:
	@echo "==> Cleaning build artifacts"
	@find . -name '__pycache__' -type d -exec $(RMR) {} +
	@find . -name '.DS_Store' -type f -exec $(RM) {} +
	@find . -name '.ipynb_checkpoints' -type d -prune -exec $(RMR) {} +
	@find . -name '.pytest_cache' -type d -prune -exec $(RMR) {} +
	@$(RMR) $(CLEAN_DIR_TARGETS)

.PHONY: lite-clean
lite-clean:
	@echo "==> Cleaning JupyterLite build artifacts"
	@$(RMR) $(LITE_CLEAN_DIR_TARGETS)

.PHONY: realclean
realclean: lite-clean clean
	@echo "==> Deep cleaning: removing .venv and deployment worktree"
#	@git worktree remove "$(WORKTREE)" --force 2>/dev/null || true
	@$(RMR) $(REALCLEAN_DIR_TARGETS)
