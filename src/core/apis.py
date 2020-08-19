from drf_core.apis import (
    CommonViewSet,
    FilteringViewSet,
    AuthenticationViewSet,
)

from core.pagination.custom_pagination import CustomPagination


class BaseViewSet(CommonViewSet, FilteringViewSet, AuthenticationViewSet):
    """
    Base viewset should be used for normal cases.
    """
    pagination_class = CustomPagination

