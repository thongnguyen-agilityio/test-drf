from drf_core import factories
from orders.models import (
    Order,
    OrderItem,
)
from accounts.factories import UserFactory
from app.constants import OrderStatusesEnum
from products.factories import ProductFactory


# =============================================================================
# Order
# =============================================================================
class OrderFactory(factories.ModelFactory):
    # Factory data for Order model.

    user = factories.SubFactory(UserFactory)
    status = factories.FuzzyChoice(OrderStatusesEnum.values())
    total_amount = factories.FuzzyInteger(1000, 2000)

    class Meta:
        model = Order
        django_get_or_create = (
            'user',
            'status',
            'total_amount',
        )


# =============================================================================
# OrderItem
# =============================================================================
class OrderItemFactory(factories.ModelFactory):
    # Factory data for OrderItem model.

    order = factories.SubFactory(OrderFactory)
    product = factories.SubFactory(ProductFactory)
    quantity = factories.FuzzyInteger(10, 50)

    class Meta:
        model = OrderItem
        django_get_or_create = (
            'order',
            'product',
            'quantity',
        )


class CartItemFactory(OrderItemFactory):
    pass


# =============================================================================
# Cart
# =============================================================================
class CartFactory(OrderFactory):
    status = OrderStatusesEnum.SHOPPING.value

    class Meta:
        model = Order
        django_get_or_create = (
            'user',
            'total_amount',
        )
