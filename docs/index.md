# Reactive Resume Python SDK

Welcome to the documentation for the unofficial **Reactive Resume Python SDK** (`rxresume-python`).

This SDK is a clean, modern, and type-safe client library for programmatically interacting with a **Reactive Resume v4** instance. It provides both synchronous and asynchronous HTTP clients powered by `httpx` and leverages `pydantic` v2 for robust data validation.

---

## Key Features

- ⚡ **Asynchronous First**: First-class async support designed for modern frameworks like FastAPI.
- 🚀 **Synchronous Fallback**: Fully featured synchronous client for simple scripts and cron jobs.
- 🛡️ **Type Safety**: Strictly typed schemas representing users and resumes via Pydantic V2.
- 🧱 **SOLID Design**: Decoupled api modules and centralized exception mapper translating API responses into clean Python exceptions.

---

## Installation

Install the package via `pip` or your favorite package manager:

```bash
pip install rxresume-python
```

Ensure your environment satisfies the requirement of **Python 3.10+**.
