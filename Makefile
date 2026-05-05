HAS_UV := $(shell command -v uv >/dev/null 2>&1; if [ $$? -eq 0 ]; then echo "true"; else echo "false"; fi)
ifeq ($(HAS_UV), true)
    PIP = uv pip
else
    PIP = pip
endif

.PHONY: install run test lint format

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

run:
	cd src && python -m server

test:
	PYTHONPATH=. $(PYTHON) -m pytest tests/ -v

lint:
	PYTHONPATH=. $(VENV)/bin/ruff check src/ tests/

format:
	PYTHONPATH=. $(VENV)/bin/ruff format src/ tests/
	PYTHONPATH=. $(VENV)/bin/ruff check --fix src/ tests/
