from django.db.models import Q
from rest_framework import status
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView)
from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.container.models import Container, Trip
from core.utils.read_exif import get_exif_dumps, get_exif_path_url
from .pagination import ContainerPageNumberPagination, TripPageNumberPagination
from .serializers import (
    ContainerListSerializer,
    ContainerCreateUpdateSerializer,
    ContainerDetailSerializer,
    TripListSerializer,
    TripDetailSerializer,
    create_trip_serializer,
    TripCreateUpdateSerializer)


# ---------------API BOAT --------------------------
class ContainerCreateAPIView(CreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerCreateUpdateSerializer


class ContainerDetailAPIView(RetrieveAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerDetailSerializer
    lookup_field = 'identifier_mac'
    lookup_url_kwarg = 'identifier_mac'


class ContainerUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerCreateUpdateSerializer
    lookup_field = 'identifier_mac'
    lookup_url_kwarg = 'identifier_mac'


class ContainerDeleteAPIView(DestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerDetailSerializer
    lookup_field = 'identifier_mac'


class ContainerListAPIView(ListAPIView):
    serializer_class = ContainerListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    search_fields = ['identifier_mac', 'name_mac', 'number_mac']
    pagination_class = ContainerPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Container.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(identifier_mac__icontains=query) |
                Q(name_mac__icontains=query) |
                Q(number_mac__icontains=query)
            ).distinct()
        return queryset_list


# ---------------API TRIP --------------------------

class TripCreateAPIView(CreateAPIView):
    queryset = Trip.objects.all()

    def get_serializer_class(self):
        return create_trip_serializer()


class TripDetailAPIView(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripDetailSerializer


class TripGroupByMacAPIView(ListAPIView):
    serializer_class = TripListSerializer
    lookup_url_kwarg = 'identifier_mac'
    pagination_class = TripPageNumberPagination

    def get_queryset(self):
        identifier_mac = self.kwargs['identifier_mac']
        trip = Trip.objects.filter(container__identifier_mac=identifier_mac)
        if not trip.exists():
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Trip.objects.filter(container__identifier_mac=identifier_mac)
            return queryset


class TripGroupByDateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        identifier_mac = kwargs['identifier_mac']
        trip = Trip.objects.filter(container__identifier_mac=identifier_mac)
        if not trip.exists():
            content = {'It has not found any record associated with this mac'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            trip = Trip.objects.filter(container__identifier_mac=identifier_mac).values_list('datetime_image',
                                                                                             flat=True)
            print(trip)
            return Response(trip)


class TripUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripCreateUpdateSerializer

    def put(self, request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        picture = request.data['picture']
        if picture:
            trip.picture.delete()
        return super(TripUpdateAPIView, self).update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        url = get_exif_path_url(instance.picture)
        instance.metadata = get_exif_dumps(url)
        instance.save()


class TripDeleteAPIView(DestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripDetailSerializer


class TripListAPIView(ListAPIView):
    serializer_class = TripListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    search_fields = ['container', 'datetime_image']
    pagination_class = ContainerPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Trip.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(container__icontains=query) |
                Q(datetime_image__icontains=query)
            ).distinct()
        return queryset_list
