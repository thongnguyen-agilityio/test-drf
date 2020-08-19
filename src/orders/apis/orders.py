from rest_framework.decorators import action

from core.apis import BaseViewSet
from utils.custom_exceptions import (
    OrderNotFoundException,
    CancelOrderDeniedException,
    PayOrderDeniedException,
)
from app.constants import OrderStatusesEnum
from orders.models import (
    Order,
    Transaction,
)
from orders.serializers import (
    OrderSerializer,
    TransactionSerializer,
    MyOrderSerializer,
)
from orders.filters import (
    OrderFiltering,
    TransactionFiltering,
)


# =============================================================================
# Order
# =============================================================================
class OrderViewSet(BaseViewSet):
    # Order ViewSet

    queryset = Order.objects.non_archived_only()
    serializer_class = OrderSerializer
    filter_class = OrderFiltering
    http_method_names = ['get', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'orders'


class MyOrderViewSet(BaseViewSet):
    # My Order ViewSet

    serializer_class = MyOrderSerializer
    filter_class = OrderFiltering
    http_method_names = ['get', 'put', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'orders/me'
    
    def list(self, request, *args, **kwargs):
        return super(MyOrderViewSet, self).list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super(MyOrderViewSet, self).retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """
        Get queryset for the current user
        """
        current_user_obj = self.request.user
        return Order.objects.non_archived_only().filter(user=current_user_obj)

    @action(
        methods=['PUT'],
        detail=True,
    )
    def cancel(self, request, *args, **kwargs):
        """
        Cancel an order.

        Only the order is in the waiting list can be canceled.
        """
        order_id = kwargs.get('pk', None)

        try:
            order_obj = self.get_queryset().get(pk=order_id)
            is_waiting_order = order_obj.status == OrderStatusesEnum.WAITING.value
            if is_waiting_order:
                order_obj.status = OrderStatusesEnum.CANCELED.value
                order_obj.save()
                return self.create_response(data={'order_id': order_obj.id})
            else:
                raise CancelOrderDeniedException()
        except Exception:
            raise OrderNotFoundException(
                developer_message='Order not found.',
                user_message='This order is not available.'
            )

    @action(
        methods=['PUT'],
        detail=True,
    )
    def payment(self, request, *args, **kwargs):
        """
        Pay an order.
        Note: This is the simple API to finalize the work flow. The real problem
        might be complexer.
        """
        order_id = kwargs.get('pk', None)

        try:
            order_obj = self.get_queryset().get(pk=order_id)

            # Only allow to pay order if it is status is in progress or shipping
            can_pay = order_obj.status in [
                OrderStatusesEnum.IN_PROGRESS.value,
                OrderStatusesEnum.SHIPPING.value,
            ]

            if can_pay:
                order_obj.status = OrderStatusesEnum.PAID.value
                order_obj.save()
                return self.create_response(data={'order_id': order_obj.id})
            else:
                raise PayOrderDeniedException()
        except Exception:
            raise OrderNotFoundException(
                developer_message='Order not found.',
                user_message='This order is not available.'
            )


# =============================================================================
# Transaction
# =============================================================================
class TransactionViewSet(BaseViewSet):
    # Transaction ViewSet

    queryset = Transaction.objects.non_archived_only()
    serializer_class = TransactionSerializer
    filter_class = TransactionFiltering
    http_method_names = ['get', 'post', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'transactions'


apps = [
    OrderViewSet,
    MyOrderViewSet,
    TransactionViewSet,
]
