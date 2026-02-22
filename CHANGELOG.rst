Changelog
=========

Unreleased ()
--------------
  * switch Makefile execution to uv extras (`dev`, `docs`, `lite`) and remove venv-ready prereqs
  * add shared Makefile target lists for pytest, pylint, YAML, and RST checks
  * replace hardcoded `rm`/`find ... -delete`/`find ... -exec rm` cleanup calls with `$(RM)` and `$(RMR)`
  * raise package minimum Python to 3.10 and declare support for Python 3.10 through 3.14
  * set CI matrix testing to Python 3.10 and 3.14; set publish/docs/citation runtimes to 3.14
  * update dependency ranges for docs/lite extras and use `rstcheck[sphinx,toml]` in dev extras
  * add release dates to all version headings in this changelog

1.0.1 (2026-01-14)
------------------
  * remove requirements*.txt, all deps in pyproject.toml
  * update readthedocs configuration
  * update docs/conf.py
  * update github actions
  * improve update_citation.py
  * move jupyter_lite_config.json to ofiber folder

1.0.0 (2025-12-01)
------------------
  * Jupyterlite support
  * improve citation
  * add make lab target
  * add make readme target for images
  * simplify ronchi-dynamic and foucault-dynamic
  * fix README so code is correct
  * bump minimum python to 3.9 
  * fix zenodo links in README
  * use venv for packaging and testing
  * remove setup.py and setup.sh
  * no longer package test files
  * clean up MANIFEST.IN
  * improve pyproject.toml
  * requirements-dev.txt is now complete

0.9.0 (2023-10-07)
------------------
  * restructure module
  * add citation
  * add conda support
  * add github test action
  * add github pypi action
  * add github citation action
  * add copyright stuff
  * add ruff support
  * overall linting of files
  * use build.os for .readthedocs
  * add more badges, tweak colors

v0.5.1 (2021-08-07)
-------------------
  * create pure python packaging
  * include wheel file
  * package as python3 only
  * fix flake8 warnings
  * add pypi badge
  * add new targets
  * automate notebook checking

v0.5.0 (2021-04-12)
-------------------
  * initial check-in
  * basic functionality for Ronchi tests
  * basic functionality for Foucault knife edge tests
