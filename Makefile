.PHONY: help install install-dev test lint format clean docs

help:
	@echo "SourceScribe Development Commands"
	@echo ""
	@echo "  install      Install package"
	@echo "  install-dev  Install package with dev dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linters"
	@echo "  format       Format code"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Generate documentation"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v

test-cov:
	pytest --cov=sourcescribe --cov-report=html --cov-report=term tests/

lint:
	ruff check sourcescribe/
	mypy sourcescribe/

format:
	black sourcescribe/ tests/
	ruff check --fix sourcescribe/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	sourcescribe generate . --output ./docs/generated
