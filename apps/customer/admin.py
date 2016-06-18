from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeAdminForm, UserCreationAdminForm
from .models import (
    User, UserProfile
)


class MyUserAdmin(UserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm

    list_display = (
        'email', 'first_name', 'password', 'last_name', 'is_admin', 'is_active', 'date_joined', 'last_login',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin',
                                       'groups', 'permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'permissions',)


admin.site.register(User, MyUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cell', 'thumb', 'is_deleted']

