from django.conf.urls import url, include

from .views import (
    IndexView, UploadImagesView, AssignUserView, AssignBoatView,
    ReportTurtleView, ReportClientView, ReportGeneralView,
    ReportRangeDateView
)

from apps.menu.views import (
    GroupModuleView, GroupView,
    GroupEditView, GroupListView,
    GroupModuleEditView, GroupModuleListView,
    GroupModuleFormsetView,
)

from apps.customer.views import (
    UserEditView, UserListView, UserView,
)

from apps.container.views import (
    ViewerBoatView, EditorBoatView,
    ContainerEditView, ContainerListView, ContainerView,
    TripEditView, TripListView, TripView,
)

administrator_patterns = ([
    url(r'^index/$', IndexView.as_view(), name="index"),
], 'administrator')

viewer_patterns = ([
    url(r'^index/$', ViewerBoatView.as_view(), name="viewer-boat"),
], 'viewer')

editor_patterns = ([
    url(r'^index/$', EditorBoatView.as_view(), name="editor-boat"),
], 'editor')

user_patterns = ([
    url(r'^assign-user/$', AssignUserView.as_view(), name="assign-user"),
    url(r'^assign-boat/$', AssignBoatView.as_view(), name="assign-boat"),
], 'users')

report_patterns = ([
    url(r'^report-turtle/$', ReportTurtleView.as_view(), name="report-turtle"),
    url(r'^report-client/$', ReportClientView.as_view(), name="report-client"),
    url(r'^report-general/$', ReportGeneralView.as_view(), name="report-general"),
    url(r'^report-range-date/$', ReportRangeDateView.as_view(), name="report-range-date"),
], 'report')

upload_patterns = ([
    url(r'^index/$', UploadImagesView.as_view(), name="upload-image"),
], 'uploads')


maintenance_patterns = ([

    url(r'^user/', include([
        url(r'^index/$', UserView.as_view(),
            name="maintenance-user"),
        url(r'^edit/$', UserEditView.as_view(),
            name="maintenance-user-edit"),
        url(r'^list/$', UserListView.as_view(),
            name="maintenance-user-list"),
    ])),

    url(r'^group/', include([
        url(r'^index/$', GroupView.as_view(),
            name="maintenance-group"),
        url(r'^edit/$', GroupEditView.as_view(),
            name="maintenance-group-edit"),
        url(r'^list/$', GroupListView.as_view(),
            name="maintenance-group-list"),
    ])),

    url(r'^group-module/', include([
        url(r'^index/$', GroupModuleView.as_view(),
            name="maintenance-group-module"),
        url(r'^edit/$', GroupModuleEditView.as_view(),
            name="maintenance-group-module-edit"),
        url(r'^list/$', GroupModuleListView.as_view(),
            name="maintenance-group-module-list"),
        url(r'^formset-submodule/$', GroupModuleFormsetView.as_view(),
            name="maintenance-group-module-formset-submodule"),
    ])),

    url(r'^container/', include([
        url(r'^index/$', ContainerView.as_view(),
            name="maintenance-container"),
        url(r'^edit/$', ContainerEditView.as_view(),
            name="maintenance-container-edit"),
        url(r'^list/$', ContainerListView.as_view(),
            name="maintenance-container-list"),

    ])),

    url(r'^trip/', include([
        url(r'^index/$', TripView.as_view(),
            name="maintenance-trip"),
        url(r'^edit/$', TripEditView.as_view(),
            name="maintenance-trip-edit"),
        url(r'^list/$', TripListView.as_view(),
            name="maintenance-trip-list"),

    ])),

], 'maintenance')


urlpatterns = [
    url(r'^dashboard/', include(administrator_patterns)),
    url(r'^maintenance/', include(maintenance_patterns)),
    url(r'^viewer/', include(viewer_patterns)),
    url(r'^editor/', include(editor_patterns)),
    url(r'^uploads/', include(upload_patterns)),
    url(r'^user/', include(user_patterns)),
    url(r'^user/api/', include('apps.customer.api.urls')),
    url(r'^container/api/', include('apps.container.api.urls')),
    url(r'^reports/', include(report_patterns)),

]
