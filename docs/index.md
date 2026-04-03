---
layout: default
title: Home
nav_order: 1
---

# django-airports-xtd

Airport models and worldwide airport data for Django, powered by [OpenFlights](http://openflights.org/).

This package provides `Airport`, `TrainStation`, and `Port` models with GeoDjango support, linking transport hubs to countries and cities via [django-cities-xtd](https://github.com/arthanson/django-cities-xtd).

## Compatibility

| Python | Django 5.0 | Django 5.1 | Django 5.2 | Django 6.0 |
|--------|------------|------------|------------|------------|
| 3.10   | Yes        | Yes        | Yes        | -          |
| 3.11   | Yes        | Yes        | Yes        | -          |
| 3.12   | Yes        | Yes        | Yes        | -          |
| 3.13   | -          | Yes        | Yes        | Yes        |
| 3.14   | -          | -          | Yes        | Yes        |

## Features

- **Transport Hub Models** - Airport, TrainStation, and Port with shared abstract base
- **IATA/ICAO codes**, altitude, timezone, and GeoDjango PointField
- **Automatic Import** from OpenFlights extended CSV data
- **City/Country Linking** via django-cities-xtd spatial queries
- **Admin Integration** with search and filtering for all models

## Credits

- Original django-airports by [Antonio Ercole De Luca](https://github.com/eracle)
- Airport data from [OpenFlights](http://openflights.org/)

## Table of Contents

- [Installation](installation.md)
- [Configuration](configuration.md)
- [Usage](usage.md)
- [Development](development.md)
- [Contributing](contributing.md)
- [Release Notes](release-notes.md)
