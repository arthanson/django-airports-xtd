from django.contrib import admin

from .models import Airport, Port, TrainStation


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("id", "openflights_id", "name", "iata", "icao", "city", "country", "timezone")
    search_fields = ("name", "iata", "icao")
    list_filter = ("country", "source")
    raw_id_fields = ["city"]


@admin.register(TrainStation)
class TrainStationAdmin(admin.ModelAdmin):
    list_display = ("id", "openflights_id", "name", "iata", "icao", "city", "country", "timezone")
    search_fields = ("name", "iata", "icao")
    list_filter = ("country", "source")
    raw_id_fields = ["city"]


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ("id", "openflights_id", "name", "iata", "icao", "city", "country", "timezone")
    search_fields = ("name", "iata", "icao")
    list_filter = ("country", "source")
    raw_id_fields = ["city"]
