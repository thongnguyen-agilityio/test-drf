from django.test import TestCase
from django.core.validators import ValidationError


from drf_core.factories import FuzzyText
from customers.models import Customer
from accounts.factories import UserFactory
from debugging.management.commands.initmembershiplevels import (
    Command as MembershipLevelCommand,
)


class CustomerTestCase(TestCase):
    """
    Customer model test case.
    """

    def setUp(self):
        super().setUp()

        MembershipLevelCommand.handle(None)

        # create a new user. it will also create customer.
        UserFactory()

    def tearDown(self):
        super().tearDown()

        Customer.objects.all().delete()

    def test_string_object(self):
        customer = Customer.objects.first()
        self.assertEqual(
            str(customer),
            f'customer: {customer.id}'
        )

    def test_customer_can_be_created(self):
        customer = Customer.objects.first()

        # Check customer
        self.assertEqual(customer.id, 1)
        self.assertTrue(isinstance(customer, Customer))

    def test_customer_can_be_updated(self):
        update_data = {
            'name': FuzzyText('customer').fuzz(),
            'is_active': False,
            'total_earned_point': 3000,
        }

        customer = Customer.objects.first()

        for key, value in update_data.items():
            setattr(customer, key, value)

        customer.save()
        customer.refresh_from_db()

        # Check customer updated data
        self.assertEqual(customer.name, update_data['name'])
        self.assertEqual(customer.is_active, update_data['is_active'])
        self.assertEqual(customer.total_earned_point,
                         update_data['total_earned_point'])
        self.assertNotEqual(customer.membership, None)

    def test_customer_can_be_deleted(self):
        customer = Customer.objects.first()
        customer.delete()

        # Check customer deleted data
        customer = Customer.objects.first()
        self.assertEqual(customer, None)

    def test_validation_error_field_type(self):
        """
        Test the validation of model.
        """
        data = {
            'is_active': FuzzyText().fuzz(),
        }

        customer = Customer(**data)
        try:
            customer.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)

    def test_validation_error_field_value_out_of_scope(self):
        """
        Test the validation of model with the field value out of scope.
        """
        data = {
            'name': FuzzyText('', 200).fuzz(),
            'email': None,
            'is_active': FuzzyText().fuzz(),
        }

        customer = Customer(**data)
        try:
            customer.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)
