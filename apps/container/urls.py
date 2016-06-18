from django.conf.urls import url

from .views import (
    ViewerBoatView, EditorBoatView
)

urlpatterns = (
    [
        url(r'^viewer/', ViewerBoatView.as_view(), name="viewer-boat"),

        url(r'^editor/$', EditorBoatView.as_view(), name="editor-boat"),
    ]
)
