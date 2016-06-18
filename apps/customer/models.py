from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, Permission)
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.db import models
from django.db.models import Count
from django.utils.encoding import force_text
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from apps.menu.models import GroupModule, GroupSubModule, SubModule, GroupState
from core import constants as core_constants
from core.utils.fields import BaseModel
from core.utils.uploads import upload_location_profile
from core.models import Zone, Country, State, Company
from .manager import UserManager

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('Email Address'), max_length=255,
                              unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=40, blank=True,
                                  null=True, unique=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True,
                                 null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=14,
                                    blank=True, null=True, unique=False)
    is_active = models.BooleanField(_('Active'), default=True, help_text=_(
        'Designates whether this users should be treated as '
        'active. Unselect this instead of deleting profiles.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)
    is_admin = models.BooleanField(_('Is_admin'), default=False)
    groups = models.ManyToManyField(
        GroupState, verbose_name=_('Groups'), blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('User Permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('users')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        full_name = u'{0:s} {1:s}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def guess_display_name(self):
        if self.display_name:
            return
        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0])
        elif self.first_name:
            dn = self.first_name
        else:
            dn = 'You'
        self.display_name = dn.strip()

    def activate(self):
        self.is_active = True
        self.save()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_groups(self):
        return self.groups.filter(current_status=core_constants.ENABLED)

    def get_menu(self):
        group_all = self.get_groups()
        group_modules = GroupModule.objects.filter(group__in=group_all).values(
            'module').annotate(dcount=Count('module'))
        self.result = dict()
        for group_module in group_modules.iterator():
            module_group = group_module['module']
            gp_modules = GroupModule.objects.filter(module=module_group)
            for gp_module in gp_modules.iterator():
                order = gp_module.module.order
                module = gp_module.module
                if module not in self.result.keys():
                    self.result[order] = list()
                add_module_dict = dict(module=dict(text=module.text,
                                                   style=module.style,
                                                   match=module.match,
                                                   submodule=dict()))
                self.result[order].append(add_module_dict)
            group_submodules = GroupSubModule.objects.filter(
                group_module__in=gp_modules
            ).values('submodule').annotate(dcount=Count('submodule'))
            for group_submodule in group_submodules.iterator():
                sub_module = SubModule.objects.get(
                    pk=group_submodule['submodule'])
                sub_order = sub_module.module.order
                sub_reference = sub_module.reference
                dict_sub_menu = self.result[sub_order][0]['module']['submodule']

                if sub_module.reference not in dict_sub_menu.keys():
                    dict_sub_menu[sub_reference] = list()
                add_module_dict = dict(text=sub_module.text,
                                       style=sub_module.style,
                                       match=sub_module.match)
                dict_sub_menu[sub_reference].append(add_module_dict)
        return self.result

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def name(self):
        if self.first_name:
            return self.first_name
        elif self.display_name:
            return self.display_name
        return 'You'


class User(CustomUser):
    class Meta(CustomUser.Meta):
        swappable = AUTH_USER_MODEL
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User, unique=True, db_index=True,
        related_name="%(app_label)s_%(class)s_user",
        on_delete=False)
    document_type = models.CharField(
        max_length=20, null=True, blank=True,
        choices=core_constants.SELECT_DEFAULT + core_constants.CODE_IDENTITY_DOCUMENT_LIST)
    document_number = models.CharField(max_length=20, null=True, blank=True)
    cell = models.CharField(max_length=20, null=True, blank=True)
    zone = models.ForeignKey(Zone, default='', related_name="%(app_label)s_%(class)s_zone", blank=True, null=True)
    country = models.ForeignKey(
        Country, default='', related_name="%(app_label)s_%(class)s_country", blank=True, null=True)
    state = models.ForeignKey(
        State, default='', related_name="%(app_label)s_%(class)s_country", blank=True, null=True)
    company = models.ForeignKey(
        Company, related_name="%(app_label)s_%(class)s_company",
        null=True, blank=True)
    initial_date = models.DateField(auto_now=True, null=True, blank=True)
    final_date = models.DateField(auto_now=False, default='', null=True, blank=True)
    profile_image = models.ImageField(
        upload_to=upload_location_profile, blank=True, null=True)

    def get_full_name(self):
        return "{0}{1}".format(self.first_name, self.last_name)

    def get_user_email(self):
        return self.user.email

    def profile_image_exists(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return static('assets/img/uncompressed/default_profile.png')

    def thumb(self):
        if self.profile_image:
            return format_html(u'<img src="{0:s}" width=60 height=60 />'
                               .format(self.profile_image.url))
        else:
            img = static('assets/img/uncompressed/default_profile.png')
            return format_html(
                u'<img src="{0:s}" width=60 height=60 />'.format(img))

    thumb.short_description = _('Thumbnail')
    thumb.allow_tags = True

    def __str__(self):
        return force_text(self.user.email)

    class Meta:
        ordering = ['date_created']
        db_table = 'user_profile'


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(
            user_id=instance.id, final_date=None)
