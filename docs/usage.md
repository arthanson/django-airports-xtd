---
layout: default
title: Usage
nav_order: 4
---

# Usage

## Importing Data

Import transport hub data from OpenFlights:

```bash
# Import airports only (default)
python manage.py airports

# Import airports and train stations
python manage.py airports --stations

# Import airports and ferry terminals
python manage.py airports --ports

# Import airports, stations, and ports
python manage.py airports --stations --ports
# or
python manage.py airports --all

# Import only stations (exclude airports)
python manage.py airports --stations --no-airports

# Import only ports (exclude airports)
python manage.py airports --ports --no-airports
```

The command will:
1. Check if country and city data exists (imports via django-cities-xtd if needed)
2. Download the latest data from OpenFlights extended dataset
3. Create or update records, linking them to cities and countries
4. Report counts for each type imported

## Querying Data

### Airports

```python
from airports.models import Airport

# Get all airports
airports = Airport.objects.all()

# Find by IATA code
jfk = Airport.objects.get(iata="JFK")

# Find by ICAO code
kjfk = Airport.objects.get(icao="KJFK")

# Search by name
airports = Airport.objects.filter(name__icontains="international")

# Filter by timezone
pacific_airports = Airport.objects.filter(timezone="America/Los_Angeles")
```

### Train Stations

```python
from airports.models import TrainStation

# Get all train stations
stations = TrainStation.objects.all()

# Find stations in a country
uk_stations = TrainStation.objects.filter(country__code2="GB")

# Find stations by name
station = TrainStation.objects.filter(name__icontains="Central")
```

### Ports

```python
from airports.models import Port

# Get all ferry terminals
ports = Port.objects.all()

# Find ports in a country
uk_ports = Port.objects.filter(country__code2="GB")
```

### Spatial Queries

All models support GeoDjango spatial queries:

```python
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from airports.models import Airport, TrainStation, Port

# Find airports within 100km of a point
point = Point(-73.7781, 40.6413, srid=4326)  # JFK coordinates
nearby = Airport.objects.annotate(
    distance=Distance("location", point)
).filter(
    distance__lte=100000  # 100km in meters
).order_by("distance")

# Find nearest train station to a location
nearest_station = TrainStation.objects.annotate(
    distance=Distance("location", point)
).order_by("distance").first()

# Get airports in a specific country
us_airports = Airport.objects.filter(country__code2="US")

# Get airports in a specific city
nyc_airports = Airport.objects.filter(city__name="New York")
```

### Related Data

```python
# Access country information
airport = Airport.objects.get(iata="JFK")
print(airport.country.name)  # "United States"
print(airport.country.code2)  # "US"

# Access city information
print(airport.city.name)  # "New York"
print(airport.city.population)

# Access timezone
print(airport.timezone)  # "America/New_York"
```

## Admin Interface

The admin interface is available for all three models:

- `/admin/airports/airport/` - Airports
- `/admin/airports/trainstation/` - Train Stations
- `/admin/airports/port/` - Ferry Terminals

Each admin includes:
- List display: ID, OpenFlights ID, name, IATA, ICAO, city, country, timezone
- Search fields: name, IATA, ICAO codes
- Filter by country and data source
- Raw ID widget for city selection
