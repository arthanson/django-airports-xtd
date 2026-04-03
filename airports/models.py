from django.contrib.gis.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class TransportHub(models.Model):
    """Abstract base model for transport hubs (airports, train stations, ports)."""

    openflights_id = models.PositiveIntegerField(
        _("OpenFlights ID"),
        unique=True,
        help_text=_("Unique identifier from OpenFlights database"),
    )

    name = models.CharField(_("name"), max_length=200)

    iata = models.CharField(
        _("IATA/FAA code"),
        blank=True,
        max_length=3,
        validators=[MinLengthValidator(3)],
    )

    icao = models.CharField(
        _("ICAO code"),
        blank=True,
        max_length=4,
        validators=[MinLengthValidator(4)],
    )

    altitude = models.FloatField(_("altitude"), default=0)
    location = models.PointField(_("location"))

    country = models.ForeignKey("cities.Country", on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey("cities.City", on_delete=models.DO_NOTHING, null=True)

    timezone = models.CharField(_("timezone"), max_length=50, blank=True)
    source = models.CharField(_("data source"), max_length=20, blank=True)

    class Meta:
        abstract = True
        ordering = ["id"]

    def __str__(self):
        return self.name


class Airport(TransportHub):
    """Airport model with data from OpenFlights."""

    class Meta(TransportHub.Meta):
        verbose_name = _("airport")
        verbose_name_plural = _("airports")


class TrainStation(TransportHub):
    """Train station model with data from OpenFlights."""

    class Meta(TransportHub.Meta):
        verbose_name = _("train station")
        verbose_name_plural = _("train stations")


class Port(TransportHub):
    """Ferry terminal/port model with data from OpenFlights."""

    class Meta(TransportHub.Meta):
        verbose_name = _("port")
        verbose_name_plural = _("ports")
