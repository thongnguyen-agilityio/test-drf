from drf_core.tests import BaseTestCase
from orders.factories import OrderFactory
from orders.apis.orders import OrderViewSet


class OrderViewSetTestCase(BaseTestCase):
    resource = OrderViewSet

    def setUp(self):
        super().setUp()

        # Create a Order for testing
        OrderFactory()

    def test_get_order_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_order_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_order_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_order_forbidden(self):
        self.auth = None
        data = {}
        self.patch_json_forbidden(data=data)

    def test_delete_order_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()
