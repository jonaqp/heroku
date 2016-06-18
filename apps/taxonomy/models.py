from django.db import models

from apps.menu.models import GroupState
from core.utils.fields import BaseModel


class Kingdom(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['name']
        verbose_name_plural = "1. kingdoms"

    def __str__(self):
        return self.name


class Type(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['name']
        verbose_name_plural = "2. types"

    def __str__(self):
        return self.name


class SubType(BaseModel):
    type = models.ForeignKey(Type, related_name="%(app_label)s_%(class)s_type")
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['name']

    def __str__(self):
        return self.name


class Classification(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['name']
        verbose_name_plural = "3. classifications"

    def __str__(self):
        return self.name


class Order(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['name']
        verbose_name_plural = "4. orders"

    def __str__(self):
        return self.name


class Family(BaseModel):
    order = models.ForeignKey(
        Order, related_name="%(app_label)s_%(class)s_order")
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['order', 'name']
        verbose_name_plural = "5. familys"

    def __str__(self):
        return "{0}-{1}".format(self.order, self.name)


class FamilySpecie(BaseModel):
    family = models.ForeignKey(
        Family, related_name="%(app_label)s_%(class)s_family")
    name = models.CharField(max_length=50, null=True, blank=True)
    name_tax = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        unique_together = ['name']

    def __str__(self):
        return "{0}-{1}".format(self.name, self.name_tax)


class Mammal(BaseModel):
    kingdom = models.ForeignKey(
        Kingdom, default='', related_name="%(app_label)s_%(class)s_kingdom")
    type = models.ForeignKey(
        Type, default='', related_name="%(app_label)s_%(class)s_type")
    subtype = models.ForeignKey(
        SubType, default='', related_name="%(app_label)s_%(class)s_subtype"
    )
    classification = models.ForeignKey(
        Classification, default='',
        related_name="%(app_label)s_%(class)s_classification")
    order = models.ForeignKey(
        Order, default='', related_name="%(app_label)s_%(class)s_order")
    family = models.ForeignKey(
        Family, default='', related_name="%(app_label)s_%(class)s_family"
    )
    specie = models.ForeignKey(
        FamilySpecie, default='', related_name="%(app_label)s_%(class)s_specie"
    )
    group = models.ForeignKey(
        GroupState, default='', null=False, blank=False,
        related_name='%(app_label)s_%(class)s_group')

    class Meta:
        ordering = ['date_created']
        unique_together = ['order', 'family', 'specie', 'group']

    def __str__(self):
        return "{0}-{1}".format(self.order, self.specie)
