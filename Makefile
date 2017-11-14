.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := show-help

#################################################################################
# GLOBALS                                                                       #
#################################################################################
SHELL := /bin/bash

PACKAGE_NAME = table_enforcer
CONDA_ENV_NAME = $(PACKAGE_NAME)
CONDA_ROOT = $(shell conda info --root)
CONDA_ENV_DIR = $(CONDA_ROOT)/envs/$(CONDA_ENV_NAME)
CONDA_ENV_PY = $(CONDA_ENV_DIR)/bin/python

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif


ifeq (${CONDA_DEFAULT_ENV},$(CONDA_ENV_NAME))
PROJECT_CONDA_ACTIVE=True
else
PROJECT_CONDA_ACTIVE=False
endif

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


#################################################################################
# COMMANDS                                                                      #
#################################################################################


## alias for show-help
help: show-help

## remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test


## remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

## check typing with mypy
mypy:
	source activate $(CONDA_ENV_NAME) && \
	mypy --ignore-missing-imports $(PACKAGE_NAME)

## remove docs artifacts
clean-docs:
	$(MAKE) -C docs clean

## check style with flake8
lint:
	source activate $(CONDA_ENV_NAME) && \
	flake8 $(PACKAGE_NAME) tests

## run tests quickly with the default Python
test:
	source activate $(CONDA_ENV_NAME) && \
	pytest


## run tests on every Python version with tox
test-all:
	source activate $(CONDA_ENV_NAME) && \
	tox

## check code coverage quickly with the default Python
coverage:
	source activate $(CONDA_ENV_NAME) && \
	coverage run --source $(PACKAGE_NAME) -m pytest && \
	coverage report -m && \
	coverage html && \
	$(BROWSER) htmlcov/index.html

## generate Sphinx HTML documentation, including API docs
docs:
	rm -f docs/$(PACKAGE_NAME).rst
	rm -f docs/$(PACKAGE_NAME).*.rst
	rm -f docs/modules.rst
	source activate $(CONDA_ENV_NAME) && \
	$(MAKE) -C docs clean && \
	$(MAKE) -C docs html && \
	$(BROWSER) docs/_build/html/index.html

## compile the docs watching for changes
servedocs: docs
	source activate $(CONDA_ENV_NAME) && \
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

## package and upload a release
release: clean
	source activate $(CONDA_ENV_NAME) && \
	python setup.py sdist upload && \
	python setup.py bdist_wheel upload

## builds source and wheel package
dist: clean
	source activate $(CONDA_ENV_NAME) && \
	python setup.py sdist && \
	python setup.py bdist_wheel && \
	ls -l dist

## installs virtual environments and requirements
install: clean install-conda-env install-jupyter-kernel install-pip-reqs install-dev-reqs install-pip-editable

install-after-conda: install-jupyter-kernel install-pip-reqs install-dev-reqs install-pip-editable

install-pip-editable:
	source activate $(CONDA_ENV_NAME) && \
	pip install -e .


error_if_active_conda_env:
ifeq (True,$(PROJECT_CONDA_ACTIVE))
	$(error "This project's conda env is active." )
endif


install-conda-env:
	conda create -n $(CONDA_ENV_NAME) 'python >=3.6' --file requirements.txt --yes

install-pip-reqs:
	source activate $(CONDA_ENV_NAME) && \
	pip install -r requirements.pip.txt && \
	pip install -r requirements.dev.pip.txt


install-jupyter-kernel:
	source activate $(CONDA_ENV_NAME) && \
	conda install --file requirements.jupyter.txt --yes && \
	python -m ipykernel install --sys-prefix --name $(CONDA_ENV_NAME) --display-name "$(CONDA_ENV_NAME)"

install-dev-reqs:
	source activate $(CONDA_ENV_NAME) && \
	conda install --file requirements.dev.txt --yes


## serve the jupyter notebook
serve-notebook:
	source activate $(CONDA_ENV_NAME) && \
	jupyter notebook --notebook-dir notebooks



## uninstalls virtual environments and requirements
uninstall-conda-env: error_if_active_conda_env
	source activate $(CONDA_ENV_NAME); \
	rm -rf $$(jupyter --data-dir)/kernels/$(CONDA_ENV_NAME); \
	rm -rf $(CONDA_ENV_DIR)

## alias to test-all (purpose: minimal req for submitting a pull request)
pull-req-check: test-all


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
## Show the available make targets
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
