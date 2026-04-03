---
layout: default
title: Development
nav_order: 5
---

# Development

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [just](https://github.com/casey/just) command runner (optional but recommended)

## Getting Started

Clone the repository:

```bash
git clone https://github.com/arthanson/django-airports-xtd.git
cd django-airports-xtd
```

## Running Tests

### Quick Test (Python 3.12 + Django 5.1)

```bash
just test-quick
```

Or with Docker Compose directly:

```bash
docker compose up --build --abort-on-container-exit test-quick
```

### Full Test Matrix

```bash
just test-all
```

### Specific Python/Django Combination

```bash
just test 312 51  # Python 3.12 + Django 5.1
just test 310 50  # Python 3.10 + Django 5.0
just test 313 60  # Python 3.13 + Django 6.0
```

## Code Quality

### Linting

```bash
just lint
```

Or directly:

```bash
ruff check airports/ test_project/
```

### Formatting

```bash
just format
```

Or directly:

```bash
ruff format airports/ test_project/
ruff check --fix airports/ test_project/
```

## Docker Commands

### Start Database

```bash
just db-up
```

### Stop Database

```bash
just db-down
```

### Open Shell in Test Container

```bash
just shell
```

### Open Database Shell

```bash
just db-shell
```

### Clean Up

```bash
just clean
```

## Project Structure

```
django-airports-xtd/
├── airports/                 # Main Django app
│   ├── models.py            # Airport model
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── management/
│   │   └── commands/
│   │       └── airports.py  # Import command
│   └── migrations/
├── test_project/            # Test Django project
│   ├── manage.py
│   ├── conftest.py
│   └── test_app/
│       ├── settings.py
│       └── tests/
│           └── test_models.py
├── docs/                    # Documentation (GitHub Pages)
├── pyproject.toml           # Package configuration
├── Dockerfile               # Test container
├── docker-compose.yml       # Test matrix services
└── justfile                 # Development commands
```
