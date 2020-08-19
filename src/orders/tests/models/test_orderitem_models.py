from django.test import TestCase
from django.core.validators import ValidationError

from drf_core.factories import FuzzyInteger, FuzzyText
from orders.factories import OrderItemFactory, OrderFactory
from orders.models import OrderItem, Order
from products.factories import ProductFactory


class OrderItemTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from OrderItemFactory
        OrderItemFactory()

    def tearDown(self):
        super().tearDown()

        OrderItem.objects.all().delete()

    def test_orderitem_can_be_created(self):
        orderitem = OrderItem.objects.first()
        self.assertEqual(orderitem.id, 1)
        self.assertTrue(isinstance(orderitem.order, Order))

        order = orderitem.order
        old_order_total_amount = order.total_amount

        new_order_item = OrderItemFactory(order=order)
        order.refresh_from_db()
        self.assertEqual(order.total_amount, old_order_total_amount +
                         new_order_item.amount)

    def test_orderitem_can_be_updated(self):
        data = {
            'order': OrderFactory(),
            'product': ProductFactory(),
            'quantity': FuzzyInteger(1, 10).fuzz(),
        }

        order_item = OrderItem.objects.first()
        order = order_item.order
        old_total_amount = order.total_amount
        old_order_item_amount = order_item.amount
        OrderItem.objects.filter(pk=order_item.id).update(**data)
        updated_obj = OrderItem.objects.get(pk=order_item.id)
        new_total_amount = order.total_amount

        self.assertEqual(updated_obj.product.id, data['product'].id)
        self.assertEqual(updated_obj.quantity, data['quantity'])
        self.assertEqual(updated_obj.product.price, data['product'].price)

        # Check order total amount
        self.assertEqual(new_total_amount, old_total_amount
                         - old_order_item_amount + order_item.amount)

    def test_orderitem_can_be_deleted(self):
        order_item = OrderItem.objects.first()
        order = order_item.order
        old_total_amount = order.total_amount
        order_item.delete()

        # Check customer deleted data
        self.assertEqual(order_item.id, None)

        # Test total amount in order after delete an order item
        new_total_amount = Order.objects.get(pk=order.id).total_amount
        self.assertEqual(new_total_amount, old_total_amount - order_item.amount)

    def test_require_field(self):
        """
        Test require field
        """
        data = {
            'order': None,
            'product': None,
        }

        order_item = OrderItem(**data)
        try:
            order_item.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)

    def test_field_type(self):
        """
        Test data value.
        """
        data = {
            'quantity': FuzzyText().fuzz(),
            'copy_price': FuzzyText().fuzz(),
        }

        order_item = OrderItem(**data)
        try:
            order_item.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)

    def test_boundary_value(self):
        data = {
            'quantity': -1,
        }

        order_item = OrderItem(**data)
        try:
            order_item.full_clean()
        except ValidationError as e:
            print(e)
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)
