import pytest
from django.contrib.gis.geos import Point
from django.db import IntegrityError

from airports.models import Airport, Port, TrainStation


@pytest.mark.django_db
class TestAirportModel:
    def test_create_airport(self):
        """Test creating an Airport instance."""
        airport = Airport.objects.create(
            openflights_id=1,
            name="Test Airport",
            iata="TST",
            icao="TEST",
            altitude=100.0,
            location=Point(-73.7781, 40.6413, srid=4326),
        )
        assert airport.id is not None
        assert airport.openflights_id == 1
        assert airport.name == "Test Airport"
        assert airport.iata == "TST"
        assert airport.icao == "TEST"
        assert airport.altitude == 100.0
        assert airport.location.x == -73.7781
        assert airport.location.y == 40.6413

    def test_airport_str(self):
        """Test Airport string representation."""
        airport = Airport.objects.create(
            openflights_id=2,
            name="JFK International",
            iata="JFK",
            icao="KJFK",
            altitude=4.0,
            location=Point(-73.7781, 40.6413, srid=4326),
        )
        assert str(airport) == "JFK International"

    def test_airport_nullable_relations(self):
        """Test that country and city can be null."""
        airport = Airport.objects.create(
            openflights_id=3,
            name="Unknown Airport",
            location=Point(0, 0, srid=4326),
        )
        assert airport.country is None
        assert airport.city is None

    def test_airport_ordering(self):
        """Test that airports are ordered by id."""
        Airport.objects.create(
            openflights_id=100,
            name="Airport B",
            location=Point(0, 0, srid=4326),
        )
        Airport.objects.create(
            openflights_id=50,
            name="Airport A",
            location=Point(1, 1, srid=4326),
        )
        airports = list(Airport.objects.all())
        # Ordering is by id (auto-generated), not openflights_id
        assert airports[0].id < airports[1].id

    def test_airport_blank_codes(self):
        """Test that IATA and ICAO codes can be blank."""
        airport = Airport.objects.create(
            openflights_id=4,
            name="Small Airfield",
            iata="",
            icao="",
            location=Point(0, 0, srid=4326),
        )
        assert airport.iata == ""
        assert airport.icao == ""

    def test_airport_timezone_and_source(self):
        """Test timezone and source fields."""
        airport = Airport.objects.create(
            openflights_id=5,
            name="Airport with Metadata",
            location=Point(0, 0, srid=4326),
            timezone="America/New_York",
            source="OurAirports",
        )
        assert airport.timezone == "America/New_York"
        assert airport.source == "OurAirports"

    def test_openflights_id_unique(self):
        """Test that openflights_id must be unique."""
        Airport.objects.create(
            openflights_id=999,
            name="First Airport",
            location=Point(0, 0, srid=4326),
        )
        with pytest.raises(IntegrityError):
            Airport.objects.create(
                openflights_id=999,
                name="Duplicate Airport",
                location=Point(1, 1, srid=4326),
            )


@pytest.mark.django_db
class TestTrainStationModel:
    def test_create_train_station(self):
        """Test creating a TrainStation instance."""
        station = TrainStation.objects.create(
            openflights_id=1001,
            name="Grand Central Terminal",
            iata="ZYP",
            location=Point(-73.9772, 40.7527, srid=4326),
            timezone="America/New_York",
        )
        assert station.id is not None
        assert station.openflights_id == 1001
        assert station.name == "Grand Central Terminal"
        assert station.iata == "ZYP"

    def test_train_station_str(self):
        """Test TrainStation string representation."""
        station = TrainStation.objects.create(
            openflights_id=1003,
            name="Union Station",
            location=Point(-77.0066, 38.8973, srid=4326),
        )
        assert str(station) == "Union Station"

    def test_train_station_ordering(self):
        """Test that train stations are ordered by id."""
        TrainStation.objects.create(
            openflights_id=2000,
            name="Station B",
            location=Point(0, 0, srid=4326),
        )
        TrainStation.objects.create(
            openflights_id=1000,
            name="Station A",
            location=Point(1, 1, srid=4326),
        )
        stations = list(TrainStation.objects.all())
        assert stations[0].id < stations[1].id


@pytest.mark.django_db
class TestPortModel:
    def test_create_port(self):
        """Test creating a Port instance."""
        port = Port.objects.create(
            openflights_id=2001,
            name="Dover Ferry Terminal",
            iata="XQD",
            location=Point(1.3089, 51.1279, srid=4326),
            timezone="Europe/London",
        )
        assert port.id is not None
        assert port.openflights_id == 2001
        assert port.name == "Dover Ferry Terminal"
        assert port.iata == "XQD"

    def test_port_str(self):
        """Test Port string representation."""
        port = Port.objects.create(
            openflights_id=2003,
            name="Staten Island Ferry",
            location=Point(-74.0721, 40.6437, srid=4326),
        )
        assert str(port) == "Staten Island Ferry"

    def test_port_ordering(self):
        """Test that ports are ordered by id."""
        Port.objects.create(
            openflights_id=3000,
            name="Port B",
            location=Point(0, 0, srid=4326),
        )
        Port.objects.create(
            openflights_id=2000,
            name="Port A",
            location=Point(1, 1, srid=4326),
        )
        ports = list(Port.objects.all())
        assert ports[0].id < ports[1].id


@pytest.mark.django_db
class TestModelSeparation:
    def test_models_have_separate_tables(self):
        """Test that Airport, TrainStation, and Port use separate tables."""
        # Create one of each with the same openflights_id value
        Airport.objects.create(
            openflights_id=9999,
            name="Test Airport",
            location=Point(0, 0, srid=4326),
        )
        TrainStation.objects.create(
            openflights_id=9999,
            name="Test Station",
            location=Point(1, 1, srid=4326),
        )
        Port.objects.create(
            openflights_id=9999,
            name="Test Port",
            location=Point(2, 2, srid=4326),
        )

        # Each model should have exactly one record
        assert Airport.objects.count() == 1
        assert TrainStation.objects.count() == 1
        assert Port.objects.count() == 1

        # And they should be independent
        assert Airport.objects.get(openflights_id=9999).name == "Test Airport"
        assert TrainStation.objects.get(openflights_id=9999).name == "Test Station"
        assert Port.objects.get(openflights_id=9999).name == "Test Port"
