---
layout: default
title: Contributing
nav_order: 6
---

# Contributing

Contributions are welcome! Every little bit helps, and credit will always be given.

## Types of Contributions

### Report Bugs

Report bugs at [GitHub Issues](https://github.com/arthanson/django-airports-xtd/issues).

When reporting a bug, please include:
- Your operating system and version
- Python and Django versions
- Database backend (PostGIS version, etc.)
- Detailed steps to reproduce the bug

### Fix Bugs

Look through GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through GitHub issues for features. Anything tagged with "enhancement" is open to whoever wants to implement it.

### Write Documentation

django-airports-xtd can always use more documentation, whether as part of the official docs, in docstrings, or even blog posts and articles.

### Submit Feedback

The best way to send feedback is to [file an issue](https://github.com/arthanson/django-airports-xtd/issues).

If you're proposing a feature:
- Explain in detail how it would work
- Keep the scope as narrow as possible
- Remember that this is a volunteer-driven project

## Getting Started

1. Fork the repo on GitHub
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your_name/django-airports-xtd.git
   ```

3. Set up development environment:
   ```bash
   cd django-airports-xtd
   pip install -e ".[dev]"
   ```

4. Create a branch for your changes:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```

5. Make your changes and run tests:
   ```bash
   just test-quick
   just lint
   ```

6. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

7. Push and submit a pull request:
   ```bash
   git push origin name-of-your-bugfix-or-feature
   ```

## Pull Request Guidelines

Before submitting a pull request:

1. The pull request should include tests
2. If adding functionality, update the documentation
3. Ensure the test suite passes across the supported Python/Django matrix
4. Follow the existing code style (enforced by ruff)

## Running Tests

```bash
# Quick test
just test-quick

# Full matrix
just test-all

# Specific combination
just test 312 51
```
