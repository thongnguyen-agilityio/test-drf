from django.test import TestCase
from django.core.validators import ValidationError

from customers.factories import MembershipFactory
from customers.models import Membership


class MembershipTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from MembershipFactory
        self.membership = MembershipFactory()

    def tearDown(self):
        super().tearDown()

        Membership.objects.all().delete()

    def test_string_object(self):
        self.assertEqual(str(self.membership),
                         f'membership: {self.membership.id}')

    def test_membership_can_be_created(self):
        self.assertEqual(self.membership.id, 1)
        self.assertTrue(isinstance(self.membership, Membership))

    def test_membership_can_be_updated(self):
        updated_data = {
            'is_active': False,
        }

        # Check updated data
        for key, value in updated_data.items():
            setattr(self.membership, key, value)

        self.membership.save()

        for key, value in updated_data.items():
            self.assertEqual(getattr(self.membership, key), value)

    def test_membership_can_be_deleted(self):
        self.membership.delete()

        # Check deleted data
        self.membership = Membership.objects.first()
        self.assertEqual(self.membership, None)

    def test_validation_error_field_type(self):
        """
        Test the validation of model.
        """
        data = {
            'level': None,
        }

        membership = Membership(**data)
        try:
            membership.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)
