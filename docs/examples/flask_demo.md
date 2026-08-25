# Flask Web Application & Docker Setup

This example demonstrates how to integrate `RxResumeClient` into a Flask web application and run it locally or via Docker / Docker Compose.

---

## Overview

The Flask demo application includes:

- **SDK Configuration**: Initializes `RxResumeClient` with environment variables.
- **Resumes Dashboard**: Fetches and renders all resumes from the server (`/resumes`).
- **Resume Detail View**: Displays detailed attributes and direct PDF download link (`/resumes/<id>`).
- **Resume Import**: Form interface for importing new candidate profiles (`/import`).
- **Docker Support**: Containerized with `Dockerfile` and `docker-compose.yml`.

---

## Local Setup

### 1. Install Dependencies

Install the SDK along with the `demo` optional dependencies:

```bash
pip install -e ".[demo]"
```

or using `uv`:

```bash
uv sync --extra demo
```

### 2. Configure Environment

Set the environment variables for your Reactive Resume instance:

```bash
export RX_RESUME_URL="https://rxresu.me"
export RX_RESUME_API_KEY="your_api_key_here"
```

### 3. Run the Application

```bash
python demo/app.py
```

Access the application at `http://localhost:5000`.

---

## Docker & Docker Compose Setup

### Using Docker Compose (Recommended)

Run the demo web application with a single command:

```bash
export RX_RESUME_API_KEY="your_api_key_here"
docker compose -f demo/docker-compose.yml up --build
```

### Using Docker CLI Directly

1. Build the Docker image:

   ```bash
   docker build -t rxresume-flask-demo -f demo/Dockerfile .
   ```

2. Run the container:

   ```bash
   docker run -d -p 5000:5000 \
     -e RX_RESUME_URL="https://rxresu.me" \
     -e RX_RESUME_API_KEY="your_api_key_here" \
     rxresume-flask-demo
   ```
