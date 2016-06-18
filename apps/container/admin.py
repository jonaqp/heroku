from django.contrib import admin

from .models import Container, Trip, TripMammal, Fisher


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    pass


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    pass


@admin.register(TripMammal)
class MammalAdmin(admin.ModelAdmin):
    pass


@admin.register(Fisher)
class FisherAdmin(admin.ModelAdmin):
    pass
