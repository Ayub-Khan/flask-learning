.PHONY: help create-venv venv requirements test-quality clean
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

## Project Starts here.
create-venv: ## Creates a virtual env
	pip3 install pipenv
	pipenv --python 3.6
	pipenv --venv

venv: ## Activates the virtual env
	pipenv shell

requirements: ## Activates the virtual env
	pipenv install --dev

test-quality: ## Test code quality
	pylint . --rcfile=pylintrc
	pycodestyle . --config=.pycodestyle --show-source
	isort --check-only --recursive .

clean: ## Remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

server: ## Start the server
	python app.py

update_db: ## Updates db
	python update_db.py
