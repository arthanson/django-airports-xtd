# django-airports-xtd

Django app providing transport hub data (airports, train stations, ferry terminals) from [OpenFlights](http://openflights.org/).

**[Documentation](https://arthanson.github.io/django-airports-xtd/)** | **[PyPI](https://pypi.org/project/django-airports-xtd/)** | **[GitHub](https://github.com/arthanson/django-airports-xtd)**

## Requirements

- Python 3.10+
- Django 5.0+
- GeoDjango with PostGIS or Spatialite
- [django-cities-xtd](https://github.com/arthanson/django-cities-xtd) >= 0.7.0

## Installation

```bash
pip install django-airports-xtd
```

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

## Usage

Import data from OpenFlights:

```bash
# Import airports only (default)
python manage.py airports

# Import airports and train stations
python manage.py airports --stations

# Import airports and ferry terminals
python manage.py airports --ports

# Import all types
python manage.py airports --all
```

For detailed usage examples and spatial queries, see the [documentation](https://arthanson.github.io/django-airports-xtd/usage.html).

## Models

Three models are provided, all with GeoDjango PointField support:

| Model | Description |
|-------|-------------|
| `Airport` | Airports and airfields |
| `TrainStation` | Train stations with IATA codes |
| `Port` | Ferry terminals with IATA codes |

Common fields (shared via abstract base):

| Field | Description |
|-------|-------------|
| `id` | Django auto-generated primary key |
| `openflights_id` | Unique identifier from OpenFlights database |
| `name` | Hub name |
| `iata` | 3-character IATA code (e.g., "JFK") |
| `icao` | 4-character ICAO code (e.g., "KJFK") |
| `altitude` | Altitude in meters |
| `location` | GeoDjango PointField (SRID 4326) |
| `country` | ForeignKey to cities.Country |
| `city` | ForeignKey to cities.City |
| `timezone` | IANA timezone (e.g., "America/New_York") |
| `source` | Data source ("OurAirports", "Legacy", "User") |

## Compatibility

| Python | Django 5.0 | Django 5.1 | Django 5.2 | Django 6.0 |
|--------|------------|------------|------------|------------|
| 3.10   | Yes        | Yes        | Yes        | -          |
| 3.11   | Yes        | Yes        | Yes        | -          |
| 3.12   | Yes        | Yes        | Yes        | -          |
| 3.13   | -          | Yes        | Yes        | Yes        |
| 3.14   | -          | -          | Yes        | Yes        |

## Development

See the [development documentation](https://arthanson.github.io/django-airports-xtd/development.html) for setup instructions.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/arthanson/django-airports-xtd.git
cd django-airports-xtd

# Run tests
just test-quick

# Run linting
just lint
```

## Disclaimer

This project is not affiliated with, endorsed by, or associated with [OpenFlights](https://openflights.org/) or its maintainers. It is an independent, third-party Django integration that consumes publicly available OpenFlights data.

## License

MIT License

## Credits

- Original django-airports by [Antonio Ercole De Luca](https://github.com/eracle)
- Data from [OpenFlights](http://openflights.org/)
