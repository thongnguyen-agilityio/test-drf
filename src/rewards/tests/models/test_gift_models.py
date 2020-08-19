from django.test import TestCase
from django.core.validators import ValidationError

from rewards.factories import GiftFactory
from rewards.models import Gift
from customers.factories import MembershipFactory
from products.factories import ProductFactory


class GiftTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from GiftFactory
        GiftFactory()

    def tearDown(self):
        super().tearDown()

        Gift.objects.all().delete()

    def test_gift_can_be_created(self):
        gift = Gift.objects.first()
        self.assertEqual(gift.id, 1)

    def test_gift_can_be_updated(self):
        updated_data = {
            'membership': MembershipFactory(),
            'product': ProductFactory(),
        }

        gift_obj = Gift.objects.first()
        for key, value in updated_data.items():
            setattr(gift_obj, key, value)

        gift_obj.save()

        self.assertEqual(gift_obj.membership.id, updated_data['membership'].id)
        self.assertEqual(gift_obj.product.id, updated_data['product'].id)

    def test_gift_can_be_deleted(self):
        gift_obj = Gift.objects.first()
        gift_obj.delete()

        self.assertEqual(gift_obj.id, None)

    def test_require_fields(self):
        data = {
            'customer': None,
        }
        obj = Gift(**data)

        try:
            obj.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)
