from django.test import TestCase
from django.core.validators import ValidationError

from drf_core import factories
from accounts.models import User
from accounts.factories import UserFactory
from customers.models import Customer


class UserTestCases(TestCase):
    """
    User model test cases.
    """

    def setUp(self) -> None:
        super().setUp()

        # Create users from UserFactory
        self.user = UserFactory()

    def tearDown(self) -> None:
        super().tearDown()

        User.objects.all().delete()

    def test_user_and_customer_can_be_created(self):
        self.assertEqual(self.user.id, 1)
        customer_obj = Customer.objects.get(account=self.user.id)
        self.assertEqual(customer_obj.email.email, self.user.email)

    def test_user_can_be_updated(self):
        update_data = {
            'email': factories.Faker('email').generate(),
        }
        for key, value in update_data.items():
            setattr(self.user, key, value)

        self.user.save()
        self.assertEqual(self.user.email, update_data['email'])

        # Check customer of this user
        customer_obj = Customer.objects.filter(account=self.user)[0]
        self.assertEqual(customer_obj.email.email, update_data['email'])

    def test_user_can_be_deleted(self):
        self.user.delete()
        self.assertEqual(self.user.id, None)
        customer = Customer.objects.filter(account=self.user.id)
        self.assertEqual(len(customer), 0)
