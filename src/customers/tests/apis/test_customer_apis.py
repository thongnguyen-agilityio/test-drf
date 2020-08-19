# from drf_core.tests import BaseTestCase
# from customers.factories import CustomerFactory
# from customers.models import Customer
# from customers.apis import CustomerViewSet
#
#
# class CustomerViewSetTestCase(BaseTestCase):
#     resource = CustomerViewSet
#
#     def setUp(self):
#         super().setUp()
#
#         # Create a Customer for testing
#         CustomerFactory()
#
#     #==============================================================================
#     # API should be forbidden if user is not logged in.
#     #==============================================================================
#     def test_get_customer_forbidden(self):
#         self.auth = None
#         self.get_json_method_forbidden()
#
#     def test_post_customer_forbidden(self):
#         self.auth = None
#         data = {}
#         self.post_json_method_forbidden(data=data)
#
#     def test_put_customer_forbidden(self):
#         self.auth = None
#         data = {}
#         self.put_json_method_forbidden(data=data)
#
#     def test_patch_customer_forbidden(self):
#         self.auth = None
#         data = {}
#         self.patch_json_forbidden(data=data)
#
#     def test_delete_customer_forbidden(self):
#         self.auth = None
#         self.delete_method_forbidden()
#
#     #==============================================================================
#     # API should be success with authenticated users.
#     #==============================================================================
#     def test_get_customer_accepted(self):
#         self.get_json_ok()
#
#         # Get 1 customer.
#         customer = Customer.objects.all()
#         self.assertEqual(len(customer), 1)
#
#         # Fill in futher test cases
#
#     def test_post_customer_accepted(self):
#         data = {}
#         self.post_json_created(data=data)
#
#         # Get 2 customer.
#         customer = Customer.objects.all()
#         self.assertEqual(len(customer), 2)
#
#         # Fill in futher test cases
#
#     def test_put_customer_accepted(self):
#         data = {}
#         customer = Customer.objects.first()
#         self.put_json_ok(data=data, fragment='%d/' % customer.id)
#
#         # Get 1 customer.
#         customer = Customer.objects.all()
#         self.assertEqual(len(customer), 1)
#
#         # Fill in futher test cases
#
#     def test_delete_customer_accepted(self):
#         customer = Customer.objects.first()
#         self.delete_json_ok('%d/' % customer.id)
#
#         # Get 0 customer.
#         customer = Customer.objects.non_archived_only()
#         self.assertEqual(len(customer), 0)
#
#         # Fill in futher test cases
