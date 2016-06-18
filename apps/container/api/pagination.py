from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class ContainerLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class ContainerPageNumberPagination(PageNumberPagination):
    page_size = 20


class TripPageNumberPagination(PageNumberPagination):
    page_size = 20
