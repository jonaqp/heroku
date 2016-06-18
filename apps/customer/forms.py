from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from core.utils import uploads
from .models import (
    User, UserProfile)


class UserCreationAdminForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreationAdminForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First Name', 'required': False,
             'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last Name', 'required': False,
             'class': 'form-control'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email', 'required': True,
             'class': 'form-control'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password',
             'required': True, 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat Password',
             'required': True, 'class': 'form-control'})
        if self.instance.id:
            self.fields['email'].widget.attrs.update({'readonly': True})
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['first_name'].required = False
            self.fields['last_name'].required = False

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = _("Passwords don't match")
            self.add_error('password1', msg)
            self.add_error('password2', msg)
        return password2

    def save(self, new=False, commit=True):
        user = super(UserCreationAdminForm, self).save(commit=False)
        if new:
            user.set_password(self.cleaned_data["password1"])
        else:
            if self.cleaned_data["password1"]:
                user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeAdminForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email Address'), max_length=255)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email', 'autocomplete': 'off',
             'required': True})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Password', 'autocomplete': 'off',
             'required': True})

    def clean(self):
        email = self.cleaned_data.get('email', '')
        password = self.cleaned_data.get('password', '')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document_type'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['profile_image'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = UserProfile
        fields = ['document_type', 'document_number',
                  'cell', 'company', 'profile_image', 'zone', 'country', 'state']
        widgets = {
            "cell": forms.TextInput(attrs={'class': 'form-control'}),
            "company": forms.TextInput(attrs={'class': 'form-control'}),
            "document_number": forms.TextInput(attrs={'class': 'form-control'}),
            "zone": forms.TextInput(attrs={'class': 'form-control'}),
            "country": forms.TextInput(attrs={'class': 'form-control'}),
            "state": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        return profile


class UserProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = UserProfile
        fields = ['profile_image']

    def save(self, current_image=None, *args, **kwargs):
        profile = super(UserProfileImageForm, self).save(*args, **kwargs)
        uploads.handle_upload_remove(current_image=current_image)
        profile.save()
        return profile


class UserProfilePasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('New Password')})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Re-Password')})
        if self.instance:
            self.current_password = self.instance.password
            self.user = self.instance

    class Meta:
        model = User
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Current Password'}),
        }

    def clean_password(self):
        clean_password = self.cleaned_data.get("password")
        write_current_password = self.user.check_password(clean_password)
        if not write_current_password:
            raise forms.ValidationError("Current password not is correct")
        return clean_password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserProfilePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
