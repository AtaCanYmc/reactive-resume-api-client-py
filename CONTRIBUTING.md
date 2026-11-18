# Contributing to Reactive Resume Python SDK

Thank you for your interest in contributing to `rxresume-python`. This document provides instructions for setting up your development environment, adhering to code quality standards, and submitting pull requests.

---

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/AtaCanYmc/reactive-resume-api-client-py.git
   cd reactive-resume-api-client-py
   ```

2. Initialize virtual environment and install all dependencies:
   ```bash
   # Using uv (recommended)
   uv sync --all-extras

   # Or using standard pip
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev,demo,mcp]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Verify local installation:
   ```bash
   make test
   ```

---

## Development Automation (Makefile)

A `Makefile` is provided to standardize common development workflows:

| Command | Action |
| :--- | :--- |
| `make test` | Run the complete pytest test suite. |
| `make test-cov` | Run tests with coverage reporting. |
| `make lint` | Run Ruff linter and Bandit security scan. |
| `make format` | Apply automated code formatting with Ruff. |
| `make format-check` | Verify formatting without modifying files. |
| `make typecheck` | Run Mypy static type analysis. |
| `make audit` | Run pip-audit for dependency vulnerabilities. |
| `make check` | Run format-check, typecheck, lint, and tests in sequence. |

---

## Commit Standards (Conventional Commits)

This repository enforces Conventional Commits. Pull request titles and commit messages must follow this structure:

```
<type>(<scope>): <description>
```

### Allowed Types

- `feat`: A new feature or endpoint mapping (increments minor version).
- `fix`: A bug fix or security patch (increments patch version).
- `docs`: Documentation updates.
- `style`: Formatting changes that do not affect code logic.
- `refactor`: Code changes that neither fix bugs nor add features.
- `perf`: Performance improvements.
- `test`: Adding or correcting tests.
- `chore`: Maintenance tasks and dependency updates.
- `ci`: CI configuration and workflow adjustments.

Breaking changes are designated by appending `!` after the type (for example, `feat!(auth): change token parameter signature`), triggering a major version increment.

---

## Pull Request Guidelines

Before opening a pull request, ensure that all checks pass:

```bash
make check
```

1. Create a descriptive branch from `main`:
   ```bash
   git checkout -b feat/my-new-endpoint
   ```
2. Write unit tests in `tests/` for any new logic or endpoints.
3. Verify that all pre-commit hooks pass upon committing.
4. Open your pull request against the `main` branch using the provided PR template.
