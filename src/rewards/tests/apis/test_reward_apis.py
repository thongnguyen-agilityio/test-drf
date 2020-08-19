# from drf_core.tests import BaseTestCase
# from rewards.factories import RewardFactory
# from rewards.models import Reward
# from rewards.apis import RewardViewSet
#
#
# class RewardViewSetTestCase(BaseTestCase):
#     resource = RewardViewSet
#
#     def setUp(self):
#         super().setUp()
#
#         # Create a Reward for testing
#         RewardFactory()
#
#     #==============================================================================
#     # API should be forbidden if user is not logged in.
#     #==============================================================================
#     def test_get_reward_forbidden(self):
#         self.auth = None
#         self.get_json_method_forbidden()
#
#     def test_post_reward_forbidden(self):
#         self.auth = None
#         data = {}
#         self.post_json_method_forbidden(data=data)
#
#     def test_put_reward_forbidden(self):
#         self.auth = None
#         data = {}
#         self.put_json_method_forbidden(data=data)
#
#     def test_patch_reward_forbidden(self):
#         self.auth = None
#         data = {}
#         self.patch_json_forbidden(data=data)
#
#     def test_delete_reward_forbidden(self):
#         self.auth = None
#         self.delete_method_forbidden()
#
#     #==============================================================================
#     # API should be success with authenticated users.
#     #==============================================================================
#     def test_get_reward_accepted(self):
#         self.get_json_ok()
#
#         # Get 1 reward.
#         reward = Reward.objects.all()
#         self.assertEqual(len(reward), 1)
#
#         # Fill in futher test cases
#
#     def test_post_reward_accepted(self):
#         data = {}
#         self.post_json_created(data=data)
#
#         # Get 2 reward.
#         reward = Reward.objects.all()
#         self.assertEqual(len(reward), 2)
#
#         # Fill in futher test cases
#
#     def test_put_reward_accepted(self):
#         data = {}
#         reward = Reward.objects.first()
#         self.put_json_ok(data=data, fragment='%d/' % reward.id)
#
#         # Get 1 reward.
#         reward = Reward.objects.all()
#         self.assertEqual(len(reward), 1)
#
#         # Fill in futher test cases
#
#     def test_delete_reward_accepted(self):
#         reward = Reward.objects.first()
#         self.delete_json_ok('%d/' % reward.id)
#
#         # Get 0 reward.
#         reward = Reward.objects.non_archived_only()
#         self.assertEqual(len(reward), 0)
#
#         # Fill in futher test cases
