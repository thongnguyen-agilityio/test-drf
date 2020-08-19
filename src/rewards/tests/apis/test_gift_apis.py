# from drf_core.tests import BaseTestCase
# from rewards.factories import GiftFactory
# from rewards.models import Gift
# from rewards.apis import GiftViewSet
#
#
# class GiftViewSetTestCase(BaseTestCase):
#     resource = GiftViewSet
#
#     def setUp(self):
#         super().setUp()
#
#         # Create a Gift for testing
#         GiftFactory()
#
#     #==============================================================================
#     # API should be forbidden if user is not logged in.
#     #==============================================================================
#     def test_get_gift_forbidden(self):
#         self.auth = None
#         self.get_json_method_forbidden()
#
#     def test_post_gift_forbidden(self):
#         self.auth = None
#         data = {}
#         self.post_json_method_forbidden(data=data)
#
#     def test_put_gift_forbidden(self):
#         self.auth = None
#         data = {}
#         self.put_json_method_forbidden(data=data)
#
#     def test_patch_gift_forbidden(self):
#         self.auth = None
#         data = {}
#         self.patch_json_forbidden(data=data)
#
#     def test_delete_gift_forbidden(self):
#         self.auth = None
#         self.delete_method_forbidden()
#
#     #==============================================================================
#     # API should be success with authenticated users.
#     #==============================================================================
#     def test_get_gift_accepted(self):
#         self.get_json_ok()
#
#         # Get 1 gift.
#         gift = Gift.objects.all()
#         self.assertEqual(len(gift), 1)
#
#         # Fill in futher test cases
#
#     def test_post_gift_accepted(self):
#         data = {}
#         self.post_json_created(data=data)
#
#         # Get 2 gift.
#         gift = Gift.objects.all()
#         self.assertEqual(len(gift), 2)
#
#         # Fill in futher test cases
#
#     def test_put_gift_accepted(self):
#         data = {}
#         gift = Gift.objects.first()
#         self.put_json_ok(data=data, fragment='%d/' % gift.id)
#
#         # Get 1 gift.
#         gift = Gift.objects.all()
#         self.assertEqual(len(gift), 1)
#
#         # Fill in futher test cases
#
#     def test_delete_gift_accepted(self):
#         gift = Gift.objects.first()
#         self.delete_json_ok('%d/' % gift.id)
#
#         # Get 0 gift.
#         gift = Gift.objects.non_archived_only()
#         self.assertEqual(len(gift), 0)
#
#         # Fill in futher test cases
