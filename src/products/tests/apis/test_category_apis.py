from drf_core import factories
from drf_core.tests import BaseTestCase
from rest_framework import status

from products.factories import CategoryFactory
from products.models import Category
from products.apis import CategoryViewSet


class CategoryViewSetTestCase(BaseTestCase):
    resource = CategoryViewSet

    def setUp(self):
        super().setUp()

        # Create a Category for testing
        CategoryFactory()

    def _generate_category(self):
        data = {
            'name': factories.FuzzyText('name').fuzz(),
            'description': factories.FuzzyText('description').fuzz(),
            'parent': CategoryFactory().id
        }

        return data

    # ==========================================================================
    # API should be forbidden if user is not logged in.
    # ==========================================================================
    def test_get_category_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_category_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_category_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_category_forbidden(self):
        self.auth = None
        data = {}
        self.patch_json_forbidden(data=data)

    def test_delete_category_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()

    # ==========================================================================
    # API should be success with authenticated users.
    # ==========================================================================
    def test_get_category_accepted(self):
        self.get_json_ok()

        # Get 1 category.
        category = Category.objects.all()
        self.assertEqual(len(category), 1)

        # Fill in futher test cases

    def test_get_category_pagination_ok(self):
        self.sampling.generate_by_model(
            app_name='products',
            model_name='Category',
            sampling=100,
        )

        # Get 101 categories.
        categories = Category.objects.all()
        self.assertEqual(len(categories), 101)

        # Test default case
        resp = self.get_json_ok('', limit=10)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.assertEqual(resp_json['count'], 101)
        self.assertEqual(resp_json['previous'], None)
        self.assertEqual(type(resp_json['next']), str)
        self.assertEqual(type(resp_json['results']), list)
        self.assertEqual(len(resp_json['results']), 10)

        # Test another case
        resp = self.get_json_ok('', limit=25, offset=25)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.assertEqual(resp_json['count'], 101)
        self.assertEqual(type(resp_json['next']), str)
        self.assertEqual(type(resp_json['previous']), str)
        self.assertEqual(type(resp_json['results']), list)
        self.assertEqual(len(resp_json['results']), 25)

    def test_post_category_accepted(self):
        data = self._generate_category()
        count_before = Category.objects.all().count()
        resp = self.post_json_created(data=data)
        count_after = Category.objects.all().count()

        self.assertEqual(count_before + 1, count_after)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_put_category_accepted(self):
        data = self._generate_category()
        category = Category.objects.first()
        resp = self.put_json_ok(data=data, fragment='%d/' % category.id)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_category_accepted(self):
        category = Category.objects.first()
        self.delete_json_ok('%d/' % category.id)

        # Get 0 category.
        category = Category.objects.non_archived_only()
        self.assertEqual(len(category), 0)
