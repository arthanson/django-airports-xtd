import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.CITIES_COUNTRY_MODEL),
        migrations.swappable_dependency(settings.CITIES_CITY_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Airport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "openflights_id",
                    models.PositiveIntegerField(
                        unique=True,
                        verbose_name="OpenFlights ID",
                        help_text="Unique identifier from OpenFlights database",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                (
                    "iata",
                    models.CharField(
                        blank=True,
                        max_length=3,
                        validators=[django.core.validators.MinLengthValidator(3)],
                        verbose_name="IATA/FAA code",
                    ),
                ),
                (
                    "icao",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        validators=[django.core.validators.MinLengthValidator(4)],
                        verbose_name="ICAO code",
                    ),
                ),
                ("altitude", models.FloatField(default=0, verbose_name="altitude")),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name="location"),
                ),
                (
                    "timezone",
                    models.CharField(blank=True, max_length=50, verbose_name="timezone"),
                ),
                (
                    "source",
                    models.CharField(blank=True, max_length=20, verbose_name="data source"),
                ),
                (
                    "city",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.CITIES_CITY_MODEL,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.CITIES_COUNTRY_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "verbose_name": "airport",
                "verbose_name_plural": "airports",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TrainStation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "openflights_id",
                    models.PositiveIntegerField(
                        unique=True,
                        verbose_name="OpenFlights ID",
                        help_text="Unique identifier from OpenFlights database",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                (
                    "iata",
                    models.CharField(
                        blank=True,
                        max_length=3,
                        validators=[django.core.validators.MinLengthValidator(3)],
                        verbose_name="IATA/FAA code",
                    ),
                ),
                (
                    "icao",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        validators=[django.core.validators.MinLengthValidator(4)],
                        verbose_name="ICAO code",
                    ),
                ),
                ("altitude", models.FloatField(default=0, verbose_name="altitude")),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name="location"),
                ),
                (
                    "timezone",
                    models.CharField(blank=True, max_length=50, verbose_name="timezone"),
                ),
                (
                    "source",
                    models.CharField(blank=True, max_length=20, verbose_name="data source"),
                ),
                (
                    "city",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.CITIES_CITY_MODEL,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.CITIES_COUNTRY_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "verbose_name": "train station",
                "verbose_name_plural": "train stations",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Port",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "openflights_id",
                    models.PositiveIntegerField(
                        unique=True,
                        verbose_name="OpenFlights ID",
                        help_text="Unique identifier from OpenFlights database",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                (
                    "iata",
                    models.CharField(
                        blank=True,
                        max_length=3,
                        validators=[django.core.validators.MinLengthValidator(3)],
                        verbose_name="IATA/FAA code",
                    ),
                ),
                (
                    "icao",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        validators=[django.core.validators.MinLengthValidator(4)],
                        verbose_name="ICAO code",
                    ),
                ),
                ("altitude", models.FloatField(default=0, verbose_name="altitude")),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name="location"),
                ),
                (
                    "timezone",
                    models.CharField(blank=True, max_length=50, verbose_name="timezone"),
                ),
                (
                    "source",
                    models.CharField(blank=True, max_length=20, verbose_name="data source"),
                ),
                (
                    "city",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.CITIES_CITY_MODEL,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.CITIES_COUNTRY_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "verbose_name": "port",
                "verbose_name_plural": "ports",
                "abstract": False,
            },
        ),
    ]
