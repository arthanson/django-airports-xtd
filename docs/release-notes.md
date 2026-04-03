---
layout: default
title: Release Notes
nav_order: 7
---

# Release Notes

## 0.3.0 (2025)

**New Features:**
- Added `TrainStation` model for train stations with IATA codes
- Added `Port` model for ferry terminals with IATA codes
- Added `openflights_id` field to all models for OpenFlights database reference
- Added `timezone` and `source` fields to all models
- Import command now supports `--stations`, `--ports`, and `--all` options
- Import command uses OpenFlights extended dataset

**Changes:**
- Abstract `TransportHub` base class for shared fields
- Modern Python packaging with pyproject.toml
- Docker-based testing with PostGIS
- Ruff for linting and formatting
- Removed Python 2 compatibility code
- Added default_auto_field to AppConfig
- GitHub Pages documentation (Jekyll-based)

## 0.2.1 (2019-12-17)

- Compatibility with Django 3.0

## 0.2 (2019-09-15)

- Renamed and uploaded to PyPI

## 0.1.5 (2018-03-08)

- Initial release
- Created HISTORY.rst file

## Credits

### Development Lead

- Antonio Ercole De Luca <eracle@posteo.eu>
- Basil Shubin <basil.shubin@gmail.com>

### Contributors

- [View all contributors on GitHub](https://github.com/arthanson/django-airports-xtd/graphs/contributors)
