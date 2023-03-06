SHELL = /bin/bash
.DEFAULT_GOAL = format

ifeq ($(OS),Windows_NT)
	BIN = Scripts
else
	BIN = bin
endif

VENV = .venv
PY =$(VENV)/$(BIN)/python -m 

pkg_src = main.py api inbound dbt
tests_src = tests

isort = $(PY) isort $(pkg_src) $(tests_src)
black = $(PY) black $(pkg_src) $(tests_src)
flake8 = $(PY) flake8 $(pkg_src) $(tests_src)

auth:
	gcloud auth login --update-adc

install:
	python3.9 -m venv $(VENV) && \
		${PY} pip install --upgrade pip && \
		${PY} pip install -r requirements.txt

install_dev:
	python3.9 -m venv $(VENV) && \
		${PY} pip install --upgrade pip && \
		${PY} pip install -r requirements.txt && \
		${PY} pip install -r requirements_dev.txt

## Auto-format the source code (isort, black)
format:
	$(isort)
	$(black)

dev:
	uvicorn main:app --reload

test:
	pytest ./tests

#TODO
#ui:
#	echo "PROJECT_ID":"virksomhetsdatalaget-dev-30e3" && \
#	$(VENV)/$(BIN)/python ./scripts/download_ui.py

run_dbt:
	../.venv/bin/dbt run --profiles-dir . --target transformer
