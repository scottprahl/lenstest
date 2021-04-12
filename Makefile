SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build

pycheck:
	-pylint lenstest/lenstest.py
	-pydocstyle lenstest/lenstest.py
	-pylint lenstest/__init__.py
	-pydocstyle lenstest/__init__.py
	-pylint lenstest/ronchi.py
	-pydocstyle lenstest/ronchi.py
	-pylint lenstest/foucault.py
	-pydocstyle lenstest/foucault.py

rstcheck:
	-rstcheck README.rst
	-rstcheck CHANGELOG.rst
	-rstcheck docs/index.rst
	-rstcheck docs/changelog.rst
	-rstcheck --ignore-directives automodule docs/lenstest.rst

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf dist
	rm -rf lenstest.egg-info
	rm -rf lenstest/__pycache__
	rm -rf docs/_build/*
	rm -rf docs/api/*
	rm -rf docs/_build/.buildinfo
	rm -rf docs/_build/.doctrees
	rm -rf .tox

rcheck:
	make clean
	make rstcheck
	make pycheck
	touch docs/*ipynb
	touch docs/*rst
	make html
	check-manifest
	pyroma -d .
#	tox

.PHONY: clean check rcheck html