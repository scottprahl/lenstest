SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build

lint:
	-pylint lenstest/__init__.py
	-pylint lenstest/lenstest.py
	-pylint lenstest/ronchi.py
	-pylint lenstest/foucault.py
	-pylint tests/test_lenstest.py
	-pylint tests/test_ronchi.py
	-pylint tests/test_foucault.py

rstcheck:
	-rstcheck README.rst
	-rstcheck CHANGELOG.rst
	-rstcheck docs/index.rst
	-rstcheck docs/changelog.rst
	-rstcheck --ignore-directives automodapi docs/lenstest.rst

yamlcheck:
	-yamllint .github/workflows/citation.yaml
	-yamllint .github/workflows/pypi.yaml
	-yamllint .github/workflows/test.yaml

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	open docs/_build/index.html

clean:
	rm -rf .ipynb_checkpoints
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf __pycache__
	rm -rf dist
	rm -rf docs/_build
	rm -rf docs/api
	rm -rf docs/.ipynb_checkpoints
	rm -rf lenstest.egg-info
	rm -rf lenstest/__init__.pyc
	rm -rf lenstest/__pycache__
	rm -rf tests/__pycache__

test:
	pytest --verbose tests/test_foucault.py
	pytest --verbose tests/test_lenstest.py
	pytest --verbose tests/test_ronchi.py
	pytest --verbose tests/test_all_notebooks.py

rcheck:
	make clean
	ruff check
	make rstcheck
	make yamlcheck
	make lint
	make test
	make html
	check-manifest
	pyroma -d .

.PHONY: clean check rcheck html