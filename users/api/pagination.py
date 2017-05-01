from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )


class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 2


class UserPageNumberPaginaton(PageNumberPagination):
    page_size = 100