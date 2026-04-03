import codecs
import csv
import logging
import os

import requests
from cities.models import City, Country
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Q
from tqdm import tqdm

from ...models import Airport, Port, TrainStation

# Extended data includes airports, train stations, and ferry terminals
ENDPOINT_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat"

# Maximum distance used to filter out too distant cities.
MAX_DISTANCE_KM = 200

APP_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))

logger = logging.getLogger("airports")

# Map OpenFlights type values to our models
TYPE_MODEL_MAP = {
    "airport": Airport,
    "station": TrainStation,
    "port": Port,
}


def create_hub(
    model_class, openflights_id, longitude, latitude, name, iata, icao, altitude, city, country, timezone, source
):
    """Create or update a transport hub record."""
    point = Point(longitude, latitude, srid=4326)

    if city and not name:
        name = city.name

    if icao == r"\N":
        icao = ""
    if iata == r"\N":
        iata = ""
    if timezone == r"\N":
        timezone = ""
    if source == r"\N":
        source = ""

    try:
        altitude = round(altitude * 0.3048, 2)
    except Exception:
        altitude = 0.0

    hub, created = model_class.objects.update_or_create(
        openflights_id=openflights_id,
        defaults={
            "iata": iata,
            "icao": icao,
            "name": name,
            "altitude": altitude,
            "location": point,
            "country": country,
            "city": city,
            "timezone": timezone,
            "source": source,
        },
    )
    if created:
        logger.debug("Added %s: %s", model_class._meta.verbose_name, hub)
    return hub


def get_country(name, city):
    """Find a country by name or through the associated city."""
    qs_all = Country.objects.all()

    qs = qs_all.filter(name__iexact=name)  # first attempt
    if qs.count() == 1:
        return qs.first()

    qs = qs_all.filter(alt_names__name__iexact=name)  # second attempt
    if qs.count() == 1:
        return qs.first()

    if city is not None:
        qs = qs_all.filter(cities=city)
        if qs.count() >= 1:
            return qs.first()  # third attempt

    return None


def get_city(name, longitude, latitude):
    """Find the nearest city within MAX_DISTANCE_KM."""
    point = Point(longitude, latitude, srid=4326)

    qs_all_near = (
        City.objects.all().annotate(distance=Distance("location", point)).filter(distance__lte=MAX_DISTANCE_KM * 1000)
    )

    qs = qs_all_near.filter(name_std__iexact=name).order_by("distance")
    if qs.exists():
        return qs.first()

    qs = qs_all_near.filter(Q(name__iexact=name) | Q(alt_names__name__iexact=name)).order_by("distance")
    if qs.exists():
        return qs.first()

    return qs_all_near.order_by("distance").first()


def get_lines(download_url):
    """Stream and decode lines from the download URL."""
    req = requests.get(download_url, stream=True)
    return codecs.iterdecode(req.iter_lines(), encoding="utf-8")


def read_hubs(reader, import_types):
    """Parse transport hub data from CSV reader and yield model instances."""
    for row in reader:
        hub_type = row.get("type", "airport").strip().lower()

        # Skip types we're not importing
        if hub_type not in import_types:
            continue

        # Get the model class for this type
        model_class = TYPE_MODEL_MAP.get(hub_type)
        if model_class is None:
            logger.debug("Skipping unknown type: %s", hub_type)
            continue

        openflights_id = int(row["openflights_id"])
        latitude = float(row["latitude"])
        longitude = float(row["longitude"])
        city_name = row["city_name"]
        country_name = row["country_name"]

        name = row["name"].strip()
        iata = row["iata"].strip()
        icao = row["icao"].strip()

        try:
            altitude = int(row["altitude"].strip())
        except (ValueError, KeyError):
            altitude = 0

        timezone = row.get("tz_name", "").strip()
        source = row.get("source", "").strip()

        city = get_city(city_name, longitude=longitude, latitude=latitude)
        if city is None:
            logger.warning("%s: %s: Cannot find city: %s.", hub_type.title(), name, city_name)

        country = get_country(country_name, city)
        if country is None:
            logger.warning("%s: %s: Cannot find country: %s", hub_type.title(), name, country_name)

        hub = create_hub(
            model_class,
            openflights_id,
            longitude,
            latitude,
            name,
            iata,
            icao,
            altitude,
            city,
            country,
            timezone,
            source,
        )
        yield hub_type, hub


class Command(BaseCommand):
    # Extended format includes type and source fields
    default_format = "openflights_id,name,city_name,country_name,iata,icao,latitude,longitude,altitude,timezone,dst,tz_name,type,source"

    help = """Imports transport hub data from OpenFlights CSV into DB.

By default, imports only airports. Use --stations and --ports to include
train stations and ferry terminals from the extended dataset.

Examples:
    python manage.py airports                    # Import airports only
    python manage.py airports --stations         # Import airports and stations
    python manage.py airports --ports            # Import airports and ports
    python manage.py airports --stations --ports # Import all types
    python manage.py airports --all              # Import all types
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--stations",
            action="store_true",
            help="Include train stations in the import",
        )
        parser.add_argument(
            "--ports",
            action="store_true",
            help="Include ferry terminals/ports in the import",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Import all types (airports, stations, and ports)",
        )
        parser.add_argument(
            "--no-airports",
            action="store_true",
            help="Exclude airports from the import (use with --stations or --ports)",
        )

    def handle(self, *args, **options):
        # Determine which types to import
        import_types = set()

        if options["all"]:
            import_types = {"airport", "station", "port"}
        else:
            if not options["no_airports"]:
                import_types.add("airport")
            if options["stations"]:
                import_types.add("station")
            if options["ports"]:
                import_types.add("port")

        if not import_types:
            self.stderr.write(self.style.ERROR("No types selected for import. Use --all or remove --no-airports."))
            return

        type_names = ", ".join(sorted(import_types))
        self.stdout.write(f"Importing: {type_names}")

        logger.info("Checking countries and cities")
        if City.objects.all().count() == 0 or Country.objects.all().count() == 0:
            call_command("cities", "--import", "country,city,alt_name")

        columns = self.default_format.split(",")

        lines = get_lines(ENDPOINT_URL)

        reader = csv.DictReader(lines, dialect="excel", fieldnames=columns)

        # Count imports by type
        counts = {"airport": 0, "station": 0, "port": 0}

        for hub_type, _hub in tqdm(read_hubs(reader, import_types), desc="Importing"):
            counts[hub_type] = counts.get(hub_type, 0) + 1

        # Report results
        for hub_type in sorted(import_types):
            count = counts.get(hub_type, 0)
            label = "Train stations" if hub_type == "station" else f"{hub_type.title()}s"
            self.stdout.write(self.style.SUCCESS(f"  {label}: {count}"))
