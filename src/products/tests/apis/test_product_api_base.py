from drf_core import factories

from core.tests.base import BaseViewSetTestCase
from products.factories import (
    CategoryFactory,
    GenderFactory,
    BaseColourFactory,
    SeasonFactory,
    UsageFactory,
    ArticleTypeFactory,
)
from products.apis import ProductViewSet
from products.models import (
    Product,
    Category,
    Gender,
    BaseColour,
    Season,
    Usage,
    ArticleType
)


class ProductViewSetTestCaseBase(BaseViewSetTestCase):
    resource = ProductViewSet

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

        Product.objects.all().delete()
        Category.objects.all().delete()
        Gender.objects.all().delete()
        BaseColour.objects.all().delete()
        Season.objects.all().delete()
        Usage.objects.all().delete()
        ArticleType.objects.all().delete()

    @classmethod
    def generate_product_data(cls):
        data = {
            "name": factories.FuzzyText('name').fuzz(),
            "description": factories.FuzzyText('description').fuzz(),
            "price": factories.FuzzyFloat(100, 200).fuzz(),
            "quantity": factories.FuzzyInteger(100, 200).fuzz(),
            "sold_quantity": factories.FuzzyInteger(100, 200).fuzz(),
            "category": CategoryFactory().id,
            "gender": GenderFactory().id,
            "base_colour": BaseColourFactory().id,
            "season": SeasonFactory().id,
            "usage": UsageFactory().id,
            "article_type": ArticleTypeFactory().id
        }

        return data
