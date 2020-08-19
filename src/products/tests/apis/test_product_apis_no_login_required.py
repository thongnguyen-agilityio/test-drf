from products.factories import ProductFactory
from products.apis import ProductViewSet
from products.tests.apis.test_product_api_base import ProductViewSetTestCaseBase


class ProductViewSetTestCase(ProductViewSetTestCaseBase):
    resource = ProductViewSet

    def setUp(self):
        super().setUp()

        # Create a Product for testing
        ProductFactory()

    def tearDown(self) -> None:
        super().tearDown()

    # ==========================================================================
    # API should be forbidden if user is not logged in.
    # ==========================================================================
    def test_get_product_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_product_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_product_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_product_forbidden(self):
        self.auth = None
        data = {}
        self.patch_json_forbidden(data=data)

    def test_delete_product_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()
