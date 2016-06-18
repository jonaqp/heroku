from django.conf.urls import url

from .views import (
    ContainerListAPIView,
    ContainerCreateAPIView,
    ContainerDetailAPIView,
    ContainerDeleteAPIView,
    ContainerUpdateAPIView,
    TripListAPIView,
    TripCreateAPIView,
    TripDetailAPIView,
    TripDeleteAPIView,
    TripUpdateAPIView,
    TripGroupByMacAPIView,
    TripGroupByDateAPIView)

urlpatterns = [

    url(r'^boat/$', ContainerListAPIView.as_view(), name='api-container-list'),
    url(r'^boat/create/$', ContainerCreateAPIView.as_view(), name='api-container-create'),
    url(r'^boat/(?P<identifier_mac>\w+)/$', ContainerDetailAPIView.as_view(), name='api-container-detail'),
    url(r'^boat/(?P<identifier_mac>\w+)/edit/$', ContainerUpdateAPIView.as_view(), name='api-container-edit'),
    url(r'^boat/(?P<identifier_mac>\w+)/delete/$', ContainerDeleteAPIView.as_view(), name='api-container-delete'),

    url(r'^trip/$', TripListAPIView.as_view(), name='api-trip-list'),
    url(r'^trip/create/$', TripCreateAPIView.as_view(), name='api-trip-create'),
    url(r'^trip/(?P<identifier_mac>\w+)/list/$', TripGroupByMacAPIView.as_view(), name='api-trip-group-by-mac'),
    url(r'^trip/(?P<identifier_mac>\w+)/group-by-date/$', TripGroupByDateAPIView.as_view(), name='api-trip-group-by-date'),
    url(r'^trip/(?P<pk>[0-9a-z-]+)/$', TripDetailAPIView.as_view(), name='api-trip-detail'),
    url(r'^trip/(?P<pk>[0-9a-z-]+)/edit/$', TripUpdateAPIView.as_view(), name='api-trip-edit'),
    url(r'^trip/(?P<pk>[0-9a-z-]+)/delete/$', TripDeleteAPIView.as_view(), name='api-trip-delete'),

]
