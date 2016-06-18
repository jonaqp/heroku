from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from .forms import LoginForm
from .views import ProfileView, ProfileSettingsView, LogoutView, LoginView

urlpatterns = [
    url(r'^$', LoginView.as_view(
        form_class=LoginForm,
        success_url='/en/administrator/dashboard/index/',
    ), name="auth_login"),
    url(r'^logout/$', LogoutView.as_view(), name='auth_logout'),

    url(r'^password/change/$',
        auth_views.password_change,
        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': 'core/registration/password_reset_form.html',
         'email_template_name': 'core/registration/password_reset_email.html',
         'subject_template_name': 'core/registration/password_reset_subject.txt',
         'extra_context': {'title': 'Demo | Log In',
                           }
         },
        name='auth_password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'core/registration/password_reset_done.html',
         'extra_context': {'title': 'Demo | Log In',
                           }
         },
        name='password_reset_done'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete'),
         'template_name': 'core/registration/password_reset_confirm.html',
         'extra_context': {'title': 'Demo | Log In',
                           }
         },

        name='auth_password_reset_confirm'),
    url(r'^reset/done/$',
        auth_views.password_reset_complete,
        {'template_name': 'core/registration/password_reset_complete.html',
         'extra_context': {'title': 'Demo | Log In',
                           }
         },
        name='auth_password_reset_complete'),

    url(r'^profile/$', ProfileView.as_view(), name='auth_profile'),
    url(r'^profile/settings/$', ProfileSettingsView.as_view(), name='auth_profile_settings'),

]
