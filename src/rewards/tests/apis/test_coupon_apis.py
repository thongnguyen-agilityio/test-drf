# from drf_core.tests import BaseTestCase
# from rewards.factories import CouponFactory
# from rewards.models import Coupon
# from rewards.apis import CouponViewSet
#
#
# class CouponViewSetTestCase(BaseTestCase):
#     resource = CouponViewSet
#
#     def setUp(self):
#         super().setUp()
#
#         # Create a Coupon for testing
#         CouponFactory()
#
#     #==============================================================================
#     # API should be forbidden if user is not logged in.
#     #==============================================================================
#     def test_get_coupon_forbidden(self):
#         self.auth = None
#         self.get_json_method_forbidden()
#
#     def test_post_coupon_forbidden(self):
#         self.auth = None
#         data = {}
#         self.post_json_method_forbidden(data=data)
#
#     def test_put_coupon_forbidden(self):
#         self.auth = None
#         data = {}
#         self.put_json_method_forbidden(data=data)
#
#     def test_patch_coupon_forbidden(self):
#         self.auth = None
#         data = {}
#         self.patch_json_forbidden(data=data)
#
#     def test_delete_coupon_forbidden(self):
#         self.auth = None
#         self.delete_method_forbidden()
#
#     #==============================================================================
#     # API should be success with authenticated users.
#     #==============================================================================
#     def test_get_coupon_accepted(self):
#         self.get_json_ok()
#
#         # Get 1 coupon.
#         coupon = Coupon.objects.all()
#         self.assertEqual(len(coupon), 1)
#
#         # Fill in futher test cases
#
#     def test_post_coupon_accepted(self):
#         data = {}
#         self.post_json_created(data=data)
#
#         # Get 2 coupon.
#         coupon = Coupon.objects.all()
#         self.assertEqual(len(coupon), 2)
#
#         # Fill in futher test cases
#
#     def test_put_coupon_accepted(self):
#         data = {}
#         coupon = Coupon.objects.first()
#         self.put_json_ok(data=data, fragment='%d/' % coupon.id)
#
#         # Get 1 coupon.
#         coupon = Coupon.objects.all()
#         self.assertEqual(len(coupon), 1)
#
#         # Fill in futher test cases
#
#     def test_delete_coupon_accepted(self):
#         coupon = Coupon.objects.first()
#         self.delete_json_ok('%d/' % coupon.id)
#
#         # Get 0 coupon.
#         coupon = Coupon.objects.non_archived_only()
#         self.assertEqual(len(coupon), 0)
#
#         # Fill in futher test cases
