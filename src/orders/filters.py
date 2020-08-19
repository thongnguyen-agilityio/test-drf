from drf_core.filtering import BaseFiltering
from orders.models import (
    Order,
    OrderItem,
    Transaction,
)


# =============================================================================
# Order
# =============================================================================
class OrderFiltering(BaseFiltering):

    class Meta:
        model = Order
        exclude = []


# =============================================================================
# OrderItem
# =============================================================================
class OrderItemFiltering(BaseFiltering):

    class Meta:
        model = OrderItem
        exclude = []


# =============================================================================
# Transaction
# =============================================================================
class TransactionFiltering(BaseFiltering):

    class Meta:
        model = Transaction
        exclude = []
