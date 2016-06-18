from django.contrib.auth.models import Group
from django.db import models

from core.utils.fields import BaseModel, BaseModel4, BaseModel5


class GroupState(BaseModel5):
    group = models.OneToOneField(
        Group, unique=True, db_index=True,
        related_name="%(app_label)s_%(class)s_group",
        on_delete=False)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return str(self.group)


# @receiver(post_save, sender=Group)
# def create_group_for_state(sender, created, instance, **kwargs):
#     if created:
#         GroupState.objects.create(
#             group_id=instance.id, current_status=core_constants.ENABLED)

class Module(BaseModel4):
    order = models.IntegerField(unique=True, null=False, blank=False)

    class Meta:
        ordering = ['order']
        unique_together = ['order', 'text']


class SubModule(BaseModel4):
    module = models.ForeignKey(
        Module, related_name="%(app_label)s_%(class)s_module", )
    reference = models.CharField(
        unique=True, max_length=100, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False, default=0)

    def moduletext(self):
        return self.module.text

    class Meta:
        ordering = ['module']
        unique_together = ['reference']


class GroupModule(BaseModel):
    group = models.ForeignKey(
        GroupState, null=False, blank=False,
        related_name='%(app_label)s_%(class)s_group')
    module = models.ForeignKey(
        Module, null=False, blank=False,
        related_name='%(app_label)s_%(class)s_module')

    def get_count_submodule(self):
        return SubModule.objects.all().prefetch_related('module').count()

    class Meta:
        unique_together = ['group', 'module']
        ordering = ['date_created']


class GroupSubModule(BaseModel):
    group_module = models.ForeignKey(
        GroupModule, null=False, blank=False,
        related_name='%(app_label)s_%(class)s_group_module')
    submodule = models.ForeignKey(
        SubModule, null=False, blank=False,
        related_name='%(app_label)s_%(class)s_submodule')

    def __str__(self):
        return "{0}-{1}".format(self.group_module, self.submodule)

    class Meta:
        unique_together = ['group_module', 'submodule']
        ordering = ['date_created']
