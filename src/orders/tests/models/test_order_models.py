from django.test import TestCase
from django.core.validators import ValidationError

from drf_core import factories
from app.constants import OrderStatusesEnum
from orders.factories import OrderFactory
from orders.models import (
    Order,
    Transaction,
)
from accounts.factories import UserFactory
from accounts.models import User
from customers.models import Customer
from debugging.management.commands.initmembershiplevels import (
    Command as MembershipLevelCommand,
)


class OrderTestCase(TestCase):
    def setUp(self):
        super().setUp()

        MembershipLevelCommand.handle(None)

        # create data from OrderFactory
        OrderFactory()

    def tearDown(self):
        super().tearDown()

        Order.objects.all().delete()

    def test_order_can_be_created(self):
        order = Order.objects.first()
        self.assertEqual(order.id, 1)
        self.assertTrue(isinstance(order, Order))
        self.assertTrue(isinstance(order.user, User))

    def test_order_can_be_updated(self):
        user = UserFactory()
        customer = Customer.objects.get(account=user)
        customer.total_earned_point = 3000
        customer.save()

        data = {
            'user': user,
            'status': OrderStatusesEnum.PAID.value,
        }
        order = Order.objects.first()

        for key, value in data.items():
            setattr(order, key, value)

        order.save()

        self.assertEqual(order.user.id, data['user'].id)
        self.assertTrue(isinstance(order.user, User))
        self.assertEqual(order.status, data['status'])

        # Check transaction
        transaction = Transaction.objects.get(order=order)
        self.assertEqual(transaction.total_amount, order.total_amount)
        self.assertEqual(transaction.earning_point,
                         int(order.total_pay_amount *
                             customer.membership.level.earning_point_rate))

    def test_order_can_be_deleted(self):
        order = Order.objects.first()
        order.delete()

        order = Order.objects.first()
        self.assertEqual(order, None)

    def test_require_fields(self):
        """
        Test require field for the model.
        """
        data = {
            'user': None,
        }

        order = Order(**data)
        try:
            order.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)

    def test_field_type(self):
        """
        Test model field type
        """
        data = {
            'status': factories.FuzzyText().fuzz(),
        }

        order = Order(**data)
        try:
            order.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)
