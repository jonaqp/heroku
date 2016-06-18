import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.constants import SELECT_DEFAULT, STATUS_MODEL1, STATUS_MODEL2
from core.queryset import AuditableManager

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class TimeStampedModel(models.Model):
    date_created = models.DateTimeField(
        blank=True, null=True, editable=False, auto_now_add=True,
        verbose_name=_('date created'))
    date_modified = models.DateTimeField(
        blank=True, null=True, editable=False, auto_now=True,
        verbose_name=_('date modified'))

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.date_modified = datetime()
    #     else:
    #         self.date_created = datetime()
    #         kwargs['force_insert'] = False
    #     super(TimeStampedModel, self).save(*args, **kwargs)
    #
    # def delete(self, force=False, *args, **kwargs):
    #     self.is_deleted = True
    #     self.save()
    #     if force:
    #         super(TimeStampedModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True


class StatusCurrent(models.Model):
    current_status = models.CharField(
        max_length=10, choices=SELECT_DEFAULT + STATUS_MODEL1)

    class Meta:
        abstract = True


class StatusBillingBModel(models.Model):
    billing_status = models.CharField(
        max_length=10, choices=SELECT_DEFAULT + STATUS_MODEL2)

    class Meta:
        abstract = True


class ModuleModel(models.Model):
    text = models.CharField(max_length=20, null=True, blank=True)
    style = models.CharField(max_length=20, null=True, blank=True)
    match = models.CharField(default="#", max_length=100, null=False,
                             blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return u'{0}'.format(self.text)


class BaseModel(UUIDModel, TimeStampedModel, StatusModel):
    current = AuditableManager()
    objects = models.Manager()

    class Meta:
        abstract = True


class BaseModel2(UUIDModel, TimeStampedModel):
    current = AuditableManager()
    objects = models.Manager()

    class Meta:
        abstract = True


class BaseModel3(UUIDModel, TimeStampedModel, StatusModel, StatusBillingBModel):
    current = AuditableManager()
    objects = models.Manager()

    class Meta:
        abstract = True


class BaseModel4(UUIDModel, TimeStampedModel, StatusModel, ModuleModel):
    current = AuditableManager()
    objects = models.Manager()

    class Meta:
        abstract = True


class BaseModel5(UUIDModel, TimeStampedModel, StatusCurrent):
    current = AuditableManager()
    objects = models.Manager()

    class Meta:
        abstract = True
