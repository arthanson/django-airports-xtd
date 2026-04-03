# django-airports-xtd justfile

# Default recipe
default:
    @just --list

# Run quick tests (Python 3.12 + Django 5.1)
test-quick:
    docker compose up --build --abort-on-container-exit test-quick

# Run all test combinations
test-all:
    docker compose up --build \
        test-py310-dj50 \
        test-py310-dj51 \
        test-py310-dj52 \
        test-py311-dj50 \
        test-py311-dj51 \
        test-py311-dj52 \
        test-py312-dj50 \
        test-py312-dj51 \
        test-py312-dj52 \
        test-py313-dj51 \
        test-py313-dj52 \
        test-py313-dj60 \
        test-py314-dj52 \
        test-py314-dj60

# Run tests for specific Python and Django version
test py="312" dj="51":
    docker compose up --build --abort-on-container-exit test-py{{py}}-dj{{dj}}

# Clean up Docker resources
clean:
    docker compose down -v --remove-orphans
    docker compose rm -f

# Run ruff linter
lint:
    ruff check airports/ test_project/

# Run ruff formatter
format:
    ruff format airports/ test_project/
    ruff check --fix airports/ test_project/

# Open a shell in the test container
shell:
    docker compose run --rm test-quick bash

# Open a database shell
db-shell:
    docker compose exec db psql -U postgres airports_test

# Build all Docker images
build:
    docker compose build

# Start the database service
db-up:
    docker compose up -d db

# Stop the database service
db-down:
    docker compose down
