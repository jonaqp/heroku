from django.contrib import admin

from .models import (
    Group, Company, Port, Zone, Country, State
)

admin.site.unregister(Group)
admin.site.register(Company)
admin.site.register(Port)
admin.site.register(Zone)
admin.site.register(Country)
admin.site.register(State)
