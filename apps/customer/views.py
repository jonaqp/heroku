from json import loads
from urllib import parse as urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from apps.customer.forms import (
    UserProfileForm, UserCreationAdminForm)
from apps.customer.models import UserProfile
from core import constants as core_constants
from core.mixins import TemplateLoginRequiredMixin
from core.utils import uploads
from core.middleware.thread_user import CuserMiddleware
from .forms import (
    UserProfileImageForm, UserProfilePasswordForm)

User = get_user_model()


class ProfileView(TemplateLoginRequiredMixin):
    template_name = 'core/profile/index.html'

    def __init__(self, **kwargs):
        self.profile_group = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        profile = UserProfile.current.values_list(
            'user__groups__group__name').filter(user__email=request.user.email)
        self.profile_group = UserProfile.current.filter(
            user__groups__group__name__in=profile).distinct().prefetch_related('user')
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_group'] = self.profile_group
        return context


class ProfileSettingsView(TemplateLoginRequiredMixin):
    template_name = 'core/profile/settings.html'

    def __init__(self, **kwargs):
        self.form_profile = None
        self.current_image = None
        self.form_profile_image = None
        self.form_profile_password = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        profile = UserProfile.current.get(user__email=request.user.email)
        user = User.objects.get(pk=profile.user.id)
        self.form_profile = UserProfileForm(
            auto_id='id_profile_%s', instance=profile)
        self.form_profile_image = UserProfileImageForm(
            auto_id='id_profile_image_%s', instance=profile)
        self.form_profile_password = UserProfilePasswordForm(
            auto_id='id_profile_password_%s', instance=user)
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        current_form_send = request.POST.get('current_form_send')
        profile = UserProfile.current.get(user__email=request.user.email)
        user = User.objects.get(pk=profile.user.id)
        self.form_profile = UserProfileForm(
            auto_id='id_profile_%s', instance=profile)
        self.form_profile_image = UserProfileImageForm(
            auto_id='id_profile_image_%s', instance=profile)
        self.form_profile_password = UserProfilePasswordForm(
            auto_id='id_profile_password_%s', instance=user)

        if current_form_send == 'form_profile':
            self.form_profile = UserProfileForm(
                request.POST, auto_id='id_profile_%s', instance=profile)
            if self.form_profile.is_valid():
                self.form_profile.save()

        if current_form_send == 'form_upload':
            self.current_image = profile.profile_image
            self.form_profile_image = UserProfileImageForm(
                request.POST, request.FILES, auto_id='id_profile_image_%s',
                instance=profile)
            if self.form_profile_image.is_valid():
                form_profile_image = self.form_profile_image.save(
                    current_image=self.current_image, commit=False)
                if request.FILES:
                    uploads.handle_upload_profile(
                        name_image=form_profile_image.profile_image,
                        resize_height=100)

        if current_form_send == 'form_password':
            self.form_profile_password = UserProfilePasswordForm(
                request.POST, auto_id='id_profile_password_%s', instance=user)
            if self.form_profile_password.is_valid():
                self.form_profile.save(commit=False)
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_profile'] = self.form_profile
        context['form_profile_upload'] = self.form_profile_image
        context['form_profile_password'] = self.form_profile_password
        return context


class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'core/registration/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, ''))

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        self.set_test_cookie()
        if self.request.user.is_authenticated():
            return redirect(self.success_url)
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        CuserMiddleware.del_user()
        return super().get(request, *args, **kwargs)


class UserView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/users/user.html'

    def __init__(self, **kwargs):
        self.form_profile = None
        self.form_user = None
        self.user_all = None
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.user_all = User.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form_profile = UserProfileForm(auto_id='id_profile_%s')
        self.form_user = UserCreationAdminForm(auto_id='id_user_%s')
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.form_user = UserCreationAdminForm(
            data=request.POST, auto_id='id_user_%s')
        self.form_profile = UserProfileForm(
            data=request.POST, auto_id='id_profile_%s')
        if self.form_user.is_valid():
            user = self.form_user.save(new=True, commit=False)
            profile = UserProfile.objects.get(user=user)
            self.form_profile = UserProfileForm(
                request.POST, auto_id='id_profile_%s', instance=profile)
            if self.form_profile.is_valid():
                self.form_profile.save()
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.warning(request, core_constants.MESSAGE_TAGS['warning'])

        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_profile'] = self.form_profile
        context['form_user'] = self.form_user
        context['list_users'] = self.user_all
        return context


class UserEditView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/users/user_add.html'

    def __init__(self, **kwargs):
        self.form_profile = None
        self.user = None
        self.form_user = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        user_email = request.GET['user_email']
        self.user = User.objects.get(email=user_email)
        self.form_user = UserCreationAdminForm(
            auto_id='id_user_%s', instance=self.user)
        self.form_profile = UserProfileForm(
            auto_id='id_profile_%s', instance=self.user)
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        data = loads(request.body.decode('utf-8'))
        data_user_pk = data['form_pk']
        data_form_user = data['form']
        self.user = User.objects.get(pk=data_user_pk)
        self.form_user = UserCreationAdminForm(
            data_form_user, auto_id='id_user_%s', instance=self.user)
        self.form_profile = UserProfileForm(
            data_form_user, auto_id='id_profile_%s', instance=self.user)
        if self.form_user.is_valid():
            self.form_user.save(new=False, commit=False)
        if self.form_profile.is_valid():
            self.form_profile.save()
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.error(request, core_constants.MESSAGE_TAGS['error'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_profile'] = self.form_profile
        context['form_user'] = self.form_user
        context['form_pk'] = self.user.id
        context['btn_edit'] = core_constants.BTN_EDIT
        return context


class UserListView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/users/user_list.html'

    def __init__(self, **kwargs):
        self.user_all = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.user_all = User.objects.all()
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_users'] = self.user_all
        return context
