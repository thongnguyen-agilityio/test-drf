from django.test import TestCase

from app.constants import MembershipSettings
from customers.models import MembershipLevel
from debugging.management.commands.initmembershiplevels import Command


class MembershipLevelTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()

        # Init list of membership levels
        Command.handle(None)

    def tearDown(self) -> None:
        super().tearDown()
        MembershipLevel.objects.all().delete()

    def test_membership_level_can_be_created(self):
        """
        Test membership levels can be created to make sure they are crated like
        a linked list with the right data.
        """
        level_objs = MembershipLevel.objects.all()
        num_levels = len(MembershipSettings)

        self.assertEqual(len(level_objs), num_levels)

        previous_levels_filtered = MembershipLevel.objects.filter(previous=None)

        # Make sure just one item returned
        self.assertEqual(len(previous_levels_filtered), 1)
        previous_level_obj = previous_levels_filtered.first()

        while previous_level_obj.next:
            next_levels_filtered = MembershipLevel.objects.filter(
                previous=previous_level_obj,
            )
            next_level_obj = next_levels_filtered.first()
            self.assertEqual(len(next_levels_filtered), 1)
            self.assertGreater(next_level_obj.require_point,
                               previous_level_obj.require_point)
            previous_level_obj = next_level_obj

    def test_membership_level_can_be_updated(self):
        update_data = {
            'require_point': 1500,
            'earning_point_rate': 0.7,
            'burning_point_rate': 0.5,
        }
        level_obj = MembershipLevel.objects.first()
        for key, value in update_data.items():
            setattr(level_obj, key, value)

        level_obj.save()
        for key, value in update_data.items():
            self.assertEqual(getattr(level_obj, key), value)

    def test_memebership_level_can_be_deleted(self):
        level_obj = MembershipLevel.objects.first()
        level_obj.delete()

        self.assertEqual(level_obj.id, None)
