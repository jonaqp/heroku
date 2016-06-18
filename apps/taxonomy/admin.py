from django.contrib import admin

from .models import (
    Kingdom, Type, SubType, Classification, Order, Family, FamilySpecie, Mammal)


@admin.register(Kingdom)
class KingdomAdmin(admin.ModelAdmin):
    pass


class SubtypeInline(admin.TabularInline):
    model = SubType


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    inlines = [SubtypeInline, ]


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


class FamilySpecieInline(admin.TabularInline):
    model = FamilySpecie


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    inlines = [FamilySpecieInline, ]


@admin.register(Mammal)
class MammalAdmin(admin.ModelAdmin):
    pass
