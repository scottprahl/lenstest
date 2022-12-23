SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build

lintcheck:
	-pylint lenstest/__init__.py
	-pylint lenstest/lenstest.py
	-pylint lenstest/ronchi.py
	-pylint lenstest/foucault.py
	-pylint tests/test_lenstest.py
	-pylint tests/test_ronchi.py
	-pylint tests/test_foucault.py

doccheck:
	-pydocstyle lenstest/lenstest.py
	-pydocstyle lenstest/__init__.py
	-pydocstyle lenstest/ronchi.py
	-pydocstyle lenstest/foucault.py

rstcheck:
	-rstcheck README.rst
	-rstcheck CHANGELOG.rst
	-rstcheck docs/index.rst
	-rstcheck docs/changelog.rst
	-rstcheck --ignore-directives automodapi docs/lenstest.rst

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	open docs/_build/index.html

clean:
	rm -rf .ipynb_checkpoints
	rm -rf .pytest_cache
	rm -rf .tox
	rm -rf __pycache__
	rm -rf dist
	rm -rf lenstest.egg-info
	rm -rf lenstest/__init__.pyc
	rm -rf lenstest/__pycache__
	rm -rf docs/_build
	rm -rf docs/api
	rm -rf docs/.ipynb_checkpoints
	rm -rf tests/__pycache__

test:
	pytest

rcheck:
	make clean
	make rstcheck
	make lintcheck
	make test
	make html
	check-manifest
	pyroma -d .
#	tox

.PHONY: clean check rcheck html