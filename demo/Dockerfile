FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files to disk & buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_DEBUG=1

# Copy package root files required for installation
COPY pyproject.toml README.md LICENSE ./
COPY reactive_resume ./reactive_resume

# Upgrade pip and install package with demo dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ".[demo]"

# Copy demo application files
COPY demo ./demo

WORKDIR /app/demo

EXPOSE 5000

CMD ["python", "app.py"]
