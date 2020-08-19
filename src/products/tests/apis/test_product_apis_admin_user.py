from rest_framework import status

from products.factories import ProductFactory
from products.models import Product
from products.apis import ProductViewSet
from products.tests.apis.test_product_api_base import ProductViewSetTestCaseBase


class ProductViewSetTestCase(ProductViewSetTestCaseBase):
    resource = ProductViewSet

    def setup_session(self, **kwargs):
        super().setup_session(**{'is_superuser': True})

    def setUp(self):
        super().setUp()

        # Create a Product for testing
        ProductFactory()

    def tearDown(self):
        super().tearDown()

    # ==========================================================================
    # API should be success with authenticated users.
    # ==========================================================================
    def test_get_product_accepted(self):
        self.get_json_ok()

        # Get 1 product.
        product = Product.objects.all()
        self.assertEqual(len(product), 1)

    def test_get_product_pagination_ok(self):
        self.sampling.generate_by_model(
            app_name='products',
            model_name='Product',
            sampling=100,
        )

        # Get 101 products.
        products = Product.objects.all()
        self.assertEqual(len(products), 101)

        # Test default case
        resp = self.get_json_ok('', limit=10)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.tet_pagination(resp)

        # Test another case
        resp = self.get_json_ok('', limit=25, offset=25)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.tet_pagination(resp)

    def test_post_product_accepted(self):
        count_before = Product.objects.all().count()
        data = self.generate_product_data()
        self.post_json_created(data=data)
        count_after = Product.objects.all().count()

        self.assertEqual(count_before + 1, count_after)

    def test_put_product_accepted(self):
        data = self.generate_product_data()
        product = Product.objects.first()
        resp = self.put_json_ok(data=data, fragment='%d/' % product.id)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_product_accepted(self):
        product = Product.objects.first()
        self.delete_json_ok('%d/' % product.id)

        # Get 0 product.
        product = Product.objects.non_archived_only()
        self.assertEqual(len(product), 0)
