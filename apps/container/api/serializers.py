from __future__ import division, unicode_literals
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from apps.container.models import Container, Trip
from core.utils.funct_dates import convert_str_in_datetime
from core.utils.read_exif import get_exif_dumps, get_exif_path_url, get_exif_loads, convert_degress_to_decimal

container_edit_url = HyperlinkedIdentityField(
    view_name='api-container-edit',
    lookup_field='identifier_mac'
)
container_detail_url = HyperlinkedIdentityField(
    view_name='api-container-detail',
    lookup_field='identifier_mac'
)
container_delete_url = HyperlinkedIdentityField(
    view_name='api-container-delete',
    lookup_field='identifier_mac'
)


# ---------------API BOAT --------------------------
class ContainerListSerializer(serializers.ModelSerializer):
    port = serializers.ReadOnlyField(source='port.name')
    zone = serializers.ReadOnlyField(source='zone.name')
    country = serializers.ReadOnlyField(source='country.name')
    fisher = serializers.ReadOnlyField(source='fisher.name')
    url_edit = container_edit_url
    url_detail = container_detail_url
    url_delete = container_delete_url

    class Meta:
        model = Container
        fields = [
            'identifier_mac',
            'name_mac',
            'number_mac',
            'port',
            'zone',
            'country',
            'fisher',
            'url_detail',
            'url_edit',
            'url_delete'
        ]


class ContainerDetailSerializer(serializers.ModelSerializer):
    port = serializers.ReadOnlyField(source='port.name')
    zone = serializers.ReadOnlyField(source='zone.name')
    country = serializers.ReadOnlyField(source='country.name')
    fisher = serializers.ReadOnlyField(source='fisher.name')

    class Meta:
        model = Container
        fields = [
            'id',
            'identifier_mac',
            'name_mac',
            'number_mac',
            'port',
            'zone',
            'country',
            'fisher'
        ]


class ContainerCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = [
            'identifier_mac',
            'name_mac',
            'number_mac',
        ]


# ---------------API TRIP --------------------------
trip_edit_url = HyperlinkedIdentityField(
    view_name='api-trip-edit'
)
trip_detail_url = HyperlinkedIdentityField(
    view_name='api-trip-detail'
)
trip_delete_url = HyperlinkedIdentityField(
    view_name='api-trip-delete'
)


def create_trip_serializer():
    class TripCreateSerializer(serializers.ModelSerializer):
        picture = serializers.ImageField(max_length=None, use_url=True)

        class Meta:
            model = Trip
            fields = [
                'picture',
            ]

        def validate(self, data):
            image_trip = data.get('picture')
            if not image_trip:
                raise ValidationError(_("This is required image"))
            return data

        @staticmethod
        def get_validate_format(string_picture):
            file_base, extension = string_picture.split(".")
            picture_split_date = file_base.split("-")
            picture_split_string = picture_split_date[0]
            picture_hour = "{0}:{1}:{2}".format(
                str(picture_split_date[1]), str(picture_split_date[2]), str(picture_split_date[3]))
            picture_split_datetime = picture_split_string.split("_")
            picture_container = str(picture_split_datetime[1])
            picture_datetime = "{0}-{1}-{2}".format(
                str(picture_split_datetime[2]), str(picture_split_datetime[3]), str(picture_split_datetime[4]))
            string_datetime_now = "{0} {1}".format(str(picture_datetime), str(picture_hour))
            new_datetime = convert_str_in_datetime(string_datetime_now)
            result = dict(datetime=new_datetime, container=picture_container)
            return result

        def create(self, validated_data):
            picture = validated_data.get('picture')
            picture_format = self.get_validate_format(str(picture))
            container_mac = picture_format['container']
            date_time = picture_format['datetime']
            container = Container.objects.filter(identifier_mac=container_mac)

            if not container.exists():
                trip = Trip.create(date_time, picture, container_mac, is_new=True)
                url = get_exif_path_url(trip.picture)
                trip.metadata = get_exif_dumps(url)
                metadata_latitude = get_exif_loads(trip.metadata)[0]['exif:GPSLatitude']
                metadata_longitude = get_exif_loads(trip.metadata)[0]['exif:GPSLongitude']
                trip.latitude = convert_degress_to_decimal(metadata_latitude)
                trip.longitude = convert_degress_to_decimal(metadata_longitude)
                trip.save()
            else:
                container = Container.objects.get(identifier_mac=container_mac)
                trip = Trip.create(date_time, picture, container, is_new=False)
                url = get_exif_path_url(trip.picture)
                trip.metadata = get_exif_dumps(url)
                metadata_latitude = get_exif_loads(trip.metadata)[0]['exif:GPSLatitude']
                metadata_longitude = get_exif_loads(trip.metadata)[0]['exif:GPSLongitude']
                trip.latitude = convert_degress_to_decimal(metadata_latitude)
                trip.longitude = convert_degress_to_decimal(metadata_longitude)
                trip.save()
            return validated_data

    return TripCreateSerializer


class TripListSerializer(serializers.ModelSerializer):
    container = serializers.ReadOnlyField(source='container.identifier_mac')
    picture = serializers.ImageField(max_length=None, use_url=True)
    datetime_image = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    metadata = serializers.JSONField()
    url_edit = trip_edit_url
    url_detail = trip_detail_url
    url_delete = trip_delete_url

    class Meta:
        model = Trip
        fields = [
            'container',
            'datetime_image',
            'picture',
            'latitude',
            'longitude',
            'metadata',
            'url_detail',
            'url_edit',
            'url_delete'
        ]

    def get_picture(self, obj):
        try:
            picture = obj.picture
        except:
            picture = None
        return picture


class TripDetailSerializer(serializers.ModelSerializer):
    container = serializers.ReadOnlyField(source='container.identifier_mac')
    picture = serializers.ImageField(max_length=None, use_url=True)
    datetime_image = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Trip
        fields = [
            'id',
            'container',
            'datetime_image',
            'picture',
            'latitude',
            'longitude',
            'metadata'
        ]


class TripCreateUpdateSerializer(serializers.ModelSerializer):
    container = serializers.ReadOnlyField(source='container.identifier_mac')
    picture = serializers.ImageField(max_length=None, use_url=True)
    metadata = serializers.JSONField()

    class Meta:
        model = Trip
        fields = [
            'container',
            'datetime_image',
            'picture',
            'latitude',
            'longitude',
            'metadata'
        ]
