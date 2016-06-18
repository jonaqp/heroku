from django.contrib import admin

from core.models import Group
from .models import (
    Module, SubModule,
    GroupModule, GroupSubModule, GroupState
)


class MenuItemInline(admin.TabularInline):
    model = SubModule
    ordering = ('order',)
    extra = 0


@admin.register(Module)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["text", 'order', 'match', 'is_deleted']
    fieldsets = [
        ["Module", {
            "fields": ('text', 'order', 'style', 'match')
        }],

    ]
    inlines = [MenuItemInline, ]


@admin.register(SubModule)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = ["text", 'order', 'moduletext', 'reference', 'is_deleted']
    fieldsets = [
        ["SubModule", {
            "fields": ('text', 'module', 'order', 'style', 'match', 'reference')
        }],

    ]


class GroupSubModuleInline(admin.TabularInline):
    list_display = ['group_module', 'submodule']
    model = GroupSubModule
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(GroupSubModuleInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        if db_field.name == 'submodule':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(
                    module=request._obj_.module)
            else:
                field.queryset = field.queryset.none()
        return field


@admin.register(GroupModule)
class GroupModuleAdmin(admin.ModelAdmin):
    list_display = ['group', 'module']
    inlines = [GroupSubModuleInline, ]

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(GroupModuleAdmin, self).get_form(request, obj, **kwargs)


class GroupStateInline(admin.TabularInline):
    model = GroupState


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [GroupStateInline, ]
