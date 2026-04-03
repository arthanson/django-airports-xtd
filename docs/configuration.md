---
layout: default
title: Configuration
nav_order: 3
---

# Configuration

## Database Setup

django-airports-xtd requires a spatial database backend. The recommended setup is PostgreSQL with PostGIS.

### PostgreSQL/PostGIS

```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "your_database",
        "USER": "your_user",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### SQLite/Spatialite (Development Only)

```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": "db.sqlite3",
    }
}

SPATIALITE_LIBRARY_PATH = "mod_spatialite"
```

## Required Settings

These settings are required for django-cities-xtd integration:

```python
CITIES_COUNTRY_MODEL = "cities.Country"
CITIES_CITY_MODEL = "cities.City"
```

## Models

This package provides three models for different transport hub types, all sharing a common abstract base (`TransportHub`).

### Common Fields

All models share these fields from the abstract base:

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Django auto-generated primary key |
| `openflights_id` | PositiveIntegerField | Unique identifier from OpenFlights |
| `name` | CharField(200) | Hub name |
| `iata` | CharField(3) | IATA/FAA code (e.g., "JFK") |
| `icao` | CharField(4) | ICAO code (e.g., "KJFK") |
| `altitude` | FloatField | Altitude in meters |
| `location` | PointField | GeoDjango point (SRID 4326) |
| `country` | ForeignKey | Link to cities.Country |
| `city` | ForeignKey | Link to cities.City |
| `timezone` | CharField(50) | IANA timezone (e.g., "America/New_York") |
| `source` | CharField(20) | Data source ("OurAirports", "Legacy", "User") |

### Airport

```python
from airports.models import Airport

jfk = Airport.objects.get(iata="JFK")
us_airports = Airport.objects.filter(country__code2="US")

# Look up by OpenFlights ID
airport = Airport.objects.get(openflights_id=3797)
```

### TrainStation

```python
from airports.models import TrainStation

stations = TrainStation.objects.all()
european_stations = TrainStation.objects.filter(country__continent="EU")
```

### Port

```python
from airports.models import Port

ports = Port.objects.all()
dover = Port.objects.filter(name__icontains="Dover")
```

## Data Source

Data is imported from OpenFlights extended dataset:

```
https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat
```

The import command automatically:
- Converts altitude from feet to meters
- Matches hubs to the nearest city within 200km
- Filters by type (airport, station, port)
