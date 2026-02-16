.PHONY: test lint format install install-dev clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
