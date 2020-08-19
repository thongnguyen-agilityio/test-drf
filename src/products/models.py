import pytz
from django.db import models
from django.core.validators import MinValueValidator

from drf_core.models import (
    ContributorModel,
    QuerySet,
)
from drf_core import fields
from app.constants import RedeemKindsEnum


class ProductCommonInfoModel(ContributorModel):

    name = fields.NameField()
    description = fields.LongNameField()

    class Meta:
        abstract = True


# =============================================================================
# Category
# =============================================================================
class CategoryQuerySet(QuerySet):
    pass


class Category(ProductCommonInfoModel):

    objects = CategoryQuerySet.as_manager()

    parent = fields.ForeignKey(
        'self',
        verbose_name='Parent category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return super().__str__()


# =============================================================================
# Season
# =============================================================================
class SeasonQuerySet(QuerySet):
    pass


class Season(ProductCommonInfoModel):

    objects = SeasonQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


# =============================================================================
# Usage
# =============================================================================
class UsageQuerySet(QuerySet):
    pass


class Usage(ProductCommonInfoModel):

    objects = UsageQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


# =============================================================================
# BaseColour
# =============================================================================
class BaseColourQuerySet(QuerySet):
    pass


class BaseColour(ProductCommonInfoModel):

    objects = BaseColourQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


# =============================================================================
# ArticleType
# =============================================================================
class ArticleTypeQuerySet(QuerySet):
    pass


class ArticleType(ProductCommonInfoModel):

    objects = ArticleTypeQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


# =============================================================================
# Gender
# =============================================================================
class GenderQuerySet(QuerySet):
    pass


class Gender(ProductCommonInfoModel):

    objects = GenderQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


# =============================================================================
# Product
# =============================================================================
class ProductQuerySet(QuerySet):
    pass


class Product(ProductCommonInfoModel):

    objects = ProductQuerySet.as_manager()

    price = fields.FloatField(
        validators=[MinValueValidator(0)],
    )
    quantity = fields.IntegerField(
        validators=[MinValueValidator(0)],
    )
    sold_quantity = fields.IntegerField(
        validators=[MinValueValidator(0)],
    )
    category = fields.ForeignKey(
        Category,
        verbose_name='Product category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    gender = fields.ForeignKey(
        Gender,
        verbose_name='Product gender',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    base_colour = fields.ForeignKey(
        BaseColour,
        verbose_name='Product base colour',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    season = fields.ForeignKey(
        Season,
        verbose_name='Season',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    usage = fields.ForeignKey(
        Usage,
        verbose_name='Product usage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    article_type = fields.ForeignKey(
        ArticleType,
        verbose_name='Article type',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_published = fields.BooleanField(
        default=False,
        help_text='This is a flag which is used to determine that product is'
                  'published or not. `False`: not published; otherwise, `True`.'
    )

    def __str__(self):
        return super().__str__()


# =============================================================================
# RedeemingProduct
# =============================================================================
class RedeemingProductQuerySet(QuerySet):
    pass


class RedeemingProduct(ContributorModel):
    """
    This model store products which allow to redeem by point or coupon.
    """

    objects = RedeemingProductQuerySet.as_manager()

    product = fields.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    kind = fields.IntegerField(
        choices=RedeemKindsEnum.to_tuple(),
        default=RedeemKindsEnum.NA.value,
    )
    start_date = fields.DateTimeField(
        null=True,
        blank=True,
    )
    end_date = fields.DateTimeField(
        null=True,
        blank=True,
    )

    @property
    def is_expired(self):
        import datetime
        now = datetime.datetime.now().replace(tzinfo=pytz.UTC)

        if not self.end_date:
            return False

        return self.end_date.replace(tzinfo=pytz.UTC) > now

