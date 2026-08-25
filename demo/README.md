# Reactive Resume Flask Demo Application

This directory contains a sample Flask web application demonstrating how to integrate the [`rxresume-python`](https://github.com/AtaCanYmc/reactive-resume-api-client-py) SDK into a Python web backend.

## Features

- **SDK Configuration**: Configures `RxResumeClient` with environment variables.
- **Resume Listing**: Fetches and renders all resumes from the server (`/resumes`).
- **Resume Inspection**: Displays detailed model attributes and PDF download URLs (`/resumes/<id>`).
- **Resume Import**: Form interface for importing new candidate profiles (`/import`).

## Quick Start

### 1. Install Dependencies

Ensure `flask` and `rxresume-python` are installed:

```bash
uv sync --extra demo
```

or via pip:

```bash
pip install -e ".[demo]"
```

### 2. Configure Environment Variables

Set your Reactive Resume server URL and API Key:

```bash
export RX_RESUME_URL="https://rxresu.me"
export RX_RESUME_API_KEY="your_api_key_here"
```

### 3. Run the Web Application

```bash
python demo/app.py
```

or using Flask CLI:

```bash
flask --app demo.app run --reload --port 5000
```

Open your browser at `http://localhost:5000`.

---

## Running with Docker

### Using Docker Compose (Recommended)

1. Build and run the containerized demo:

   ```bash
   export RX_RESUME_API_KEY="your_api_key_here"
   docker compose -f demo/docker-compose.yml up --build
   ```

2. Open your browser at `http://localhost:5000`.

### Using Docker Directly

```bash
docker build -t rxresume-flask-demo -f demo/Dockerfile .

docker run -d -p 5000:5000 \
  -e RX_RESUME_URL="https://rxresu.me" \
  -e RX_RESUME_API_KEY="your_api_key_here" \
  rxresume-flask-demo
```
