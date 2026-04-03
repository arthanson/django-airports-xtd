# Dockerfile for testing django-airports-xtd
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

# Install PostGIS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml setup.py ./
COPY airports/ ./airports/
COPY test_project/ ./test_project/

# Install the package in editable mode with dev dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Default command runs tests
CMD ["pytest", "-v"]
