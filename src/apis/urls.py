from typing import List

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet

from accounts.apis import LogoutView, LoginView
from customers.apis import apps as customers_viewsets
from orders.apis.cart import apps as cart_viewsets
from orders.apis.orders import apps as orders_viewsets
from products.apis import apps as products_viewsets

api_routers = DefaultRouter()


def register_apis(list_viewsets: List[ViewSet]) -> None:
    """
    Register APIs from the list of viewsets

    @param list_viewsets: List of viewsets
    """
    for viewset in list_viewsets:
        api_routers.register(
            viewset.resource_name,
            viewset,
            viewset.resource_name,
        )


register_apis(customers_viewsets)
register_apis(cart_viewsets)
register_apis(orders_viewsets)
register_apis(products_viewsets)

urlpatterns = [
    path('logout/', LogoutView.as_view()),
    path('login/', LoginView.as_view())
]

# Collect all end-point patterns
urlpatterns += api_routers.urls
