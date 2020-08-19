from django.test import TestCase
from django.core.validators import ValidationError

from drf_core.factories import (
    FuzzyText,
    FuzzyBoolean,
)
from rewards.factories import (
    RewardFactory,
)
from rewards.models import Reward
from customers.factories import MembershipFactory


class RewardTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

        Reward.objects.all().delete()

    def test_reward_can_be_created(self):
        # create data from RewardFactory
        RewardFactory()

        reward = Reward.objects.first()
        self.assertIsNotNone(reward.id)

    def test_reward_can_be_updated(self):
        update_data = {
            'membership': MembershipFactory(),
            'is_active': FuzzyBoolean().fuzz()
        }
        reward_obj = RewardFactory()
        for key, value in update_data.items():
            setattr(reward_obj, key, value)

        reward_obj.save()
        self.assertEqual(reward_obj.membership.id, update_data['membership'].id)

    def test_reward_can_be_deleted(self):
        reward_obj = RewardFactory()
        reward_obj.delete()

        self.assertIsNone(reward_obj.id)

    def test_field_type(self):
        data = {
            'is_active': FuzzyText('', 100).fuzz(),
        }
        obj = Reward(**data)

        try:
            obj.full_clean()
        except ValidationError as e:
            for key, _ in data.items():
                self.assertTrue(key in e.message_dict)
