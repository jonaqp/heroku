from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    url(r'^', include('apps.customer.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/compressed/favicon.ico'),
        name='favicon.ico'),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'),
        name='robots.txt'),
    url(r'^sitemap\.xml$', TemplateView.as_view(
        template_name='sitemap.xml', content_type='text/xml'),
        name='sitemap-xml'),
]

urlpatterns += i18n_patterns(
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^administrator/', include('apps.dashboard.urls')),
    # url(r'^chaining/', include('smart_selects.urls')),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
