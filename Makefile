SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build

lintcheck:
	-pylint lenstest/lenstest.py
	-pylint lenstest/__init__.py
	-pylint lenstest/ronchi.py
	-pylint lenstest/foucault.py

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
	-rstcheck --ignore-directives automodule docs/lenstest.rst

notecheck:
	make clean
	pytest --verbose -n 4 test_all_notebooks.py

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	open docs/_build/index.html

clean:
	rm -rf dist
	rm -rf lenstest.egg-info
	rm -rf lenstest/__pycache__
	rm -rf docs/_build
	rm -rf docs/api
	rm -rf .tox
	rm -rf __pycache__

rcheck:
	make clean
	make notecheck
	make rstcheck
	make lintcheck
	make doccheck
	make html
	check-manifest
	pyroma -d .
#	tox

.PHONY: clean check rcheck html