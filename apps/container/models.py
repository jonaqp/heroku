from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.taxonomy.models import Mammal
from core.models import Company, Zone, Country, Port
from core.utils.fields import BaseModel
from core.utils.uploads import upload_location_trip


class Fisher(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    cellphone = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(
        Company, default='', related_name="%(app_label)s_%(class)s_company")

    def __str__(self):
        return self.name


class Container(BaseModel):
    identifier_mac = models.CharField(max_length=50, null=False, blank=False, unique=True)
    name_mac = models.CharField(max_length=50, null=True, blank=True)
    number_mac = models.CharField(max_length=50, null=True, blank=True)
    port = models.ForeignKey(
        Port, default='', related_name="%(app_label)s_%(class)s_port", blank=True, null=True)
    zone = models.ForeignKey(
        Zone, default='', related_name="%(app_label)s_%(class)s_zone", blank=True, null=True)
    country = models.ForeignKey(
        Country, default='', related_name="%(app_label)s_%(class)s_country", blank=True, null=True)
    fisher = models.ForeignKey(
        Fisher, default='', related_name="%(app_label)s_%(class)s_fisher", blank=True, null=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['identifier_mac']

    @staticmethod
    def create(identifier_mac):
        container = Container()
        container.identifier_mac = identifier_mac
        container.save()
        return container

    def __str__(self):
        return self.identifier_mac


class Trip(BaseModel):
    container = models.ForeignKey(
        Container, related_name="%(app_label)s_%(class)s_container")
    datetime_image = models.DateTimeField(auto_now=False, default='', null=False, blank=False)
    picture = models.ImageField(
        upload_to=upload_location_trip, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    metadata = JSONField(default=dict())

    class Meta:
        ordering = ['date_created']

    @staticmethod
    def create(datetime_image, picture, container, is_new=True):
        trip = Trip()
        trip.datetime_image = datetime_image
        trip.picture = picture
        new_container = container
        if container and is_new:
            new_container = Container.create(container)
        elif container and not is_new:
            new_container = new_container
        trip.container = new_container
        trip.save()
        return trip

    def __str__(self):
        return str(self.container)


class TripMammal(BaseModel):
    trip_detail_initial = models.ForeignKey(
        Trip, related_name="%(app_label)s_%(class)s_trip_mammal_initial")
    trip_detail_final = models.ForeignKey(
        Trip, related_name="%(app_label)s_%(class)s_trip_mammal_final")
    mammal = models.ForeignKey(
        Mammal, related_name="%(app_label)s_%(class)s_mammal")

    class Meta:
        ordering = ['date_created']
