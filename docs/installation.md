---
layout: default
title: Installation
nav_order: 2
---

# Installation

## Requirements

- Python 3.10+
- Django 5.0+
- GeoDjango with PostGIS or Spatialite
- [django-cities-xtd](https://github.com/arthanson/django-cities-xtd) >= 0.7.0

## System Dependencies

### Ubuntu/Debian

```bash
sudo apt-get install -y gdal-bin libgdal-dev libpq-dev
```

### macOS (with Homebrew)

```bash
brew install gdal postgis
```

## Package Installation

### From PyPI

```bash
pip install django-airports-xtd
```

### From Source

```bash
git clone https://github.com/arthanson/django-airports-xtd.git
cd django-airports-xtd
pip install -e .
```

## Django Configuration

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django.contrib.gis",
    "cities",
    "airports",
    ...
]
```

Configure the cities model settings:

```python
CITIES_COUNTRY_MODEL = "cities.Country"
CITIES_CITY_MODEL = "cities.City"
```

Run migrations:

```bash
python manage.py migrate
```
