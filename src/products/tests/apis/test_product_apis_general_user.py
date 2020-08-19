from products.factories import ProductFactory
from products.apis import ProductViewSet
from products.tests.apis.test_product_api_base import ProductViewSetTestCaseBase


class ProductViewSetTestCase(ProductViewSetTestCaseBase):
    resource = ProductViewSet

    def setUp(self):
        super().setUp()

        # Create a Product for testing
        ProductFactory()

    # ==========================================================================
    # API should be success with authenticated users.
    # ==========================================================================
    def test_get_list_product_forbidden(self):
        self.get_json_method_forbidden()

    def test_post_product_forbidden(self):
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_product_not_allowed(self):
        data = {}
        self.put_json_method_not_allowed(data=data)

    def test_patch_product_forbidden(self):
        data = {}
        resp = self.patch_json(data=data)
        self.assertHttpMethodNotAllowed(resp)

    def test_delete_product_not_allowed(self):
        self.delete_method_not_allowed()

    def test_search_product_ok(self):
        resp = self.get_json(fragment='search/')
        self.tet_pagination(resp)
