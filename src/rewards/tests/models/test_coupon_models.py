from django.test import TestCase
from django.core.validators import ValidationError

from drf_core.factories import (
    FuzzyText,
    FuzzyFloat,
    FuzzyBoolean,
    FuzzyChoice,
)
from app.constants import CouponKindsEnum
from rewards.factories import CouponFactory
from rewards.models import Coupon


class CouponTestCase(TestCase):
    Model = Coupon
    Factory = CouponFactory

    def setUp(self):
        super().setUp()

        # create data from CouponFactory
        self.Factory()

    def tearDown(self):
        super().tearDown()

        self.Model.objects.all().delete()

    def test_coupon_can_be_created(self):
        coupon = self.Model.objects.first()
        self.assertEqual(coupon.id, 1)

    def test_coupon_can_be_updated(self):
        updated_data = {
            'kind': FuzzyChoice(CouponKindsEnum.values()).fuzz(),
            'amount': FuzzyFloat(10, 1000).fuzz(),
            'target_amount': FuzzyFloat(100, 1000).fuzz(),
            'is_applied_minimum_purchase_rule': FuzzyBoolean().fuzz(),
        }
        coupon_obj = self.Model.objects.first()
        for key, value in updated_data.items():
            setattr(coupon_obj, key, value)

        coupon_obj.save()
        self.assertEqual(coupon_obj.kind, updated_data['kind'])
        self.assertEqual(coupon_obj.amount, updated_data['amount'])
        self.assertEqual(coupon_obj.target_amount, updated_data['target_amount'])
        self.assertEqual(coupon_obj.is_applied_minimum_purchase_rule,
                         updated_data['is_applied_minimum_purchase_rule'])

    def test_coupon_can_be_deleted(self):
        coupon_obj = self.Model.objects.first()
        coupon_obj.delete()

        self.assertEqual(coupon_obj.id, None)

    def test_field_type(self):
        data = {
            'kind': FuzzyText('', 100).fuzz(),
            'amount': FuzzyText('', 100).fuzz(),
            'target_amount': FuzzyText('', 100).fuzz(),
            'is_minimum_purchase': FuzzyText('', 100).fuzz(),
        }
        obj = self.Model(**data)

        try:
            obj.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)

    def test_boundary_value(self):
        data = {
            'kind': -10,
            'amount': -1,
            'target_amount': -1,
        }
        obj = self.Model(**data)

        try:
            obj.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)

