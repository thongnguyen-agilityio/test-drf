from rest_framework import status
from drf_core import factories

from app.constants import OrderStatusesEnum
from core.tests.base import BaseViewSetTestCase
from orders.factories import OrderFactory
from orders.models import Order, OrderItem
from orders.apis.orders import (
    MyOrderViewSet,
    OrderViewSet,
)
from products.models import Product


class OrderBaseTestCase(BaseViewSetTestCase):
    """
    Base test case for order
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        Product.objects.all().delete()


class OrderViewSetTestCase(OrderBaseTestCase):
    resource = OrderViewSet

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get_list_orders_of_current_user_ok(self):
        order_objs = [
            OrderFactory(
                user=self.authenticated_user,
                status=factories.FuzzyChoice(OrderStatusesEnum.values()).fuzz(),
            )
            for _ in range(30)
        ]

        resp = self.get_json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(order_objs), resp.data['count'])


class MyOrderViewSetTestCase(BaseViewSetTestCase):
    resource = MyOrderViewSet

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_put_cancel_an_order_ok(self):
        """
        Test for API PUT /api/v1/orders/me/{order_id}/cancel/
        """
        # Create an order for test
        waiting_order_obj = OrderFactory(
            user=self.authenticated_user,
            status=OrderStatusesEnum.WAITING.value,
        )

        # Cancel an order
        waiting_order_id = waiting_order_obj.id
        resp = self.put_json(data={}, fragment=f'{waiting_order_id}/cancel/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('order_id'), waiting_order_id)

    def test_put_cancel_an_order_bad_request(self):
        """
        If an user is not `Waiting` status. We cannot cancel.

        API PUT /api/v1/orders/me/{order_id}/cancel/
        """
        statuses = OrderStatusesEnum.values()
        statuses.remove(OrderStatusesEnum.WAITING.value)

        # Test for all order status except WAITING
        for order_status in statuses:
            not_waiting_order_obj = OrderFactory(
                user=self.authenticated_user,
                status=order_status,
            )

            # Cancel an order
            not_waiting_order_id = not_waiting_order_obj.id
            resp = self.put_json(data={},
                                 fragment=f'{not_waiting_order_id}/cancel/')
            self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
            self.has_valid_custom_error_response(resp)

    def test_put_pay_an_order_ok(self):
        """
        API PUT /api/v1/orders/me/{order_id}/payment/
        """
        can_pay_statuses = [
            OrderStatusesEnum.IN_PROGRESS.value,
            OrderStatusesEnum.SHIPPING.value,
        ]

        for order_status in can_pay_statuses:
            order_obj = OrderFactory(
                user=self.authenticated_user,
                status=order_status,
            )

            # Cancel an order
            order_id = order_obj.id
            resp = self.put_json(data={}, fragment=f'{order_id}/payment/')
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertEqual(resp.data.get('order_id'), order_id)

    def test_put_pay_an_order_bad_request(self):
        """
        API PUT /api/v1/orders/me/{order_id}/payment/
        """
        can_not_pay_statuses = [
            OrderStatusesEnum.SHOPPING.value,
            OrderStatusesEnum.WAITING.value,
            OrderStatusesEnum.CANCELED.value,
            OrderStatusesEnum.PAID.value,
        ]

        for order_status in can_not_pay_statuses:
            # Create order
            order_obj = OrderFactory(
                user=self.authenticated_user,
                status=order_status,
            )

            # Pay an order
            order_id = order_obj.id
            resp = self.put_json(data={}, fragment=f'{order_id}/payment/')
            self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
            self.has_valid_custom_error_response(resp)

    def test_put_pay_not_existed_order_bad_request(self):
        """
        API PUT /api/v1/orders/me/{order_id}/payment/
        """
        order_id = factories.Faker('uuid4').generate()
        resp = self.put_json(data={}, fragment=f'{order_id}/payment/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.has_valid_custom_error_response(resp)
