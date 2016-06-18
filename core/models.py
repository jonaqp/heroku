from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
    Group, Permission)
from django.db import models

from apps.menu.models import GroupModule, GroupSubModule, SubModule, GroupState
from core import constants as core_constants
from .utils.fields import BaseModel, BaseModel4, BaseModel5
from .utils.uploads import upload_location_company


class Zone(BaseModel):
    name = models.CharField(max_length=2, db_index=True,
                            choices=core_constants.CONTINENT_CHOICES)

    def __str__(self):
        return self.name


class Country(BaseModel):
    zone = models.ForeignKey(Zone, related_name="%(app_label)s_%(class)s_zone")
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    iso_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class State(BaseModel):
    zone = models.ForeignKey(Zone, default='', related_name="%(app_label)s_%(class)s_zone")
    country = models.ForeignKey(Country, default='',
                                related_name="%(app_label)s_%(class)s_country")
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Company(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    logo = models.FileField(upload_to=upload_location_company, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mobile_phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['name']
        unique_together = ['name']

    def __str__(self):
        return self.name


class Port(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
