VENV := .venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash

.PHONY: help
help: ## Display callable targets.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(BIN)/activate

.PHONY: format
format: ## Format all the code
	$(BIN)/black .

.PHONY: requirements
requirements: ## Install dependencies
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -U -r requirements.txt

.PHONY: run
run: ## Run the application locally
	$(PYTHON) -m python_retweet

.PHONY: freeze
freeze: ## Pin current dependencies
	$(BIN)/pip freeze > requirements.txt

.PHONY: clean
clean:  ## Delete the dependencies folder
	rm -rf .venv/

.PHONY: install
install: venv requirements ## This command must be launched for the first use of the project
