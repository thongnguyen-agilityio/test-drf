from datetime import datetime, timedelta
from dateutil import tz

from drf_core import factories
from app.constants import RedeemKindsEnum
from products.models import (
    Category,
    Season,
    Usage,
    BaseColour,
    ArticleType,
    Gender,
    Product,
    RedeemingProduct,
)


# =============================================================================
# Category
# =============================================================================
class CategoryFactory(factories.ModelFactory):
    # Factory data for Category model.
    name = factories.Sequence(lambda n: 'Category name %03d' % n)
    parent = None

    class Meta:
        model = Category
        django_get_or_create = (
            'name',
            'parent',
        )


# =============================================================================
# Season
# =============================================================================
class SeasonFactory(factories.ModelFactory):
    # Factory data for Season model.
    name = factories.Sequence(lambda n: 'Season name %03d' % n)

    class Meta:
        model = Season
        django_get_or_create = (
            'name',
        )


# =============================================================================
# Usage
# =============================================================================
class UsageFactory(factories.ModelFactory):
    # Factory data for Usage model.
    name = factories.Sequence(lambda n: 'Usage name %03d' % n)

    class Meta:
        model = Usage
        django_get_or_create = (
            'name',
        )


# =============================================================================
# BaseColour
# =============================================================================
class BaseColourFactory(factories.ModelFactory):
    # Factory data for BaseColour model.
    name = factories.Sequence(lambda n: 'BaseColour name %03d' % n)

    class Meta:
        model = BaseColour
        django_get_or_create = (
            'name',
        )


# =============================================================================
# ArticleType
# =============================================================================
class ArticleTypeFactory(factories.ModelFactory):
    # Factory data for ArticleType model.
    name = factories.Sequence(lambda n: 'ArticleType name %03d' % n)

    class Meta:
        model = ArticleType
        django_get_or_create = (
            'name',
        )


# =============================================================================
# Gender
# =============================================================================
class GenderFactory(factories.ModelFactory):
    # Factory data for Gender model.
    name = factories.Sequence(lambda n: 'Gender name %03d' % n)

    class Meta:
        model = Gender
        django_get_or_create = (
            'name',
        )


# =============================================================================
# Product
# =============================================================================
class ProductFactory(factories.ModelFactory):
    # Factory data for Product model.
    name = factories.Sequence(lambda n: 'Product name %03d' % n)
    price = factories.FuzzyFloat(1, 1000.0)
    quantity = factories.FuzzyInteger(50, 100)
    sold_quantity = factories.FuzzyInteger(10, 100)
    category = factories.SubFactory(CategoryFactory)
    gender = factories.SubFactory(GenderFactory)
    base_colour = factories.SubFactory(BaseColourFactory)
    season = factories.SubFactory(SeasonFactory)
    usage = factories.SubFactory(UsageFactory)
    is_published = factories.FuzzyChoice([True, False])

    class Meta:
        model = Product
        django_get_or_create = (
            'name',
            'price',
            'quantity',
            'sold_quantity',
            'category',
            'gender',
            'base_colour',
            'season',
            'usage',
            'is_published',
        )


# =============================================================================
# RedeemingProduct
# =============================================================================
class RedeemingProductFactory(factories.ModelFactory):
    # Factory data for RedeemingProduct model.
    product = factories.SubFactory(ProductFactory)
    kind = RedeemKindsEnum.COUPON.value
    start_date = None
    end_date = None

    class Meta:
        model = RedeemingProduct
        django_get_or_create = (
            'product',
            'kind',
            'start_date',
            'end_date',
        )

    class Params:
        is_point_kind = factories.Trait(
            kind=RedeemKindsEnum.POINT.value,
            start_date=factories.FuzzyDateTime(
                start_dt=datetime(2010, 11, 7, 0, 0, tzinfo=tz.UTC)),
            end_date=factories.LazyAttribute(
                lambda o: o.start_date + timedelta(days=10)
            )
        )


apps = [
    CategoryFactory,
    SeasonFactory,
    UsageFactory,
    BaseColourFactory,
    ArticleTypeFactory,
    GenderFactory,
    ProductFactory,
    RedeemingProductFactory,
]
