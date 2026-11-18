.DEFAULT_GOAL := help

# Detection for uv vs standard python environment
UV ?= $(shell command -v uv 2>/dev/null)

ifeq ($(UV),)
    RUN :=
    INSTALL_CMD := pip install -e ".[dev,demo]"
else
    RUN := uv run
    INSTALL_CMD := uv sync --all-extras
endif

.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install development, docs, and demo dependencies
	$(INSTALL_CMD)

.PHONY: test
test: ## Run unit and integration tests
	$(RUN) pytest

.PHONY: test-cov
test-cov: ## Run tests with code coverage report
	$(RUN) pytest --cov=reactive_resume --cov-report=term-missing --cov-report=xml

.PHONY: lint
lint: ## Run linter (ruff) and security scan (bandit)
	$(RUN) ruff check .
	$(RUN) bandit -r reactive_resume/ demo/ -ll

.PHONY: format
format: ## Format code with ruff
	$(RUN) ruff check --fix .
	$(RUN) ruff format .

.PHONY: format-check
format-check: ## Check code formatting without applying changes
	$(RUN) ruff format --check .
	$(RUN) ruff check .

.PHONY: typecheck
typecheck: ## Run type checking with mypy
	$(RUN) mypy reactive_resume tests

.PHONY: audit
audit: ## Run security vulnerability audit on dependencies
ifeq ($(UV),)
	pip-audit
else
	uv run --with pip-audit pip-audit
endif

.PHONY: check
check: format-check typecheck lint test ## Run all checks (format, typecheck, lint, test)

.PHONY: docs-serve
docs-serve: ## Serve documentation web app locally on port 8000
	python -m http.server 8000 --directory docs

.PHONY: docs-build
docs-build: ## Verify documentation web assets
	@test -f docs/index.html && echo "Documentation web screen verified at docs/index.html"

.PHONY: demo
demo: ## Run the Flask demo web application
	$(RUN) python demo/app.py

.PHONY: demo-docker
demo-docker: ## Build and start the demo application using Docker Compose
	docker compose -f demo/docker-compose.yml up --build

.PHONY: clean
clean: ## Clean up caches, build files, and temporary artifacts
	rm -rf build/ dist/ *.egg-info .eggs/
	rm -rf .pytest_cache .coverage coverage.xml htmlcov/
	rm -rf .mypy_cache .ruff_cache
	rm -rf site/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
