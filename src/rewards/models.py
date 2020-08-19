import uuid

from django.db import models
from django.core.validators import MinValueValidator

from drf_core.models import (
    ContributorModel,
    QuerySet,
)
from drf_core import fields
from app.constants import CouponKindsEnum
from products.models import Product
from customers.models import Membership, Customer


# =============================================================================
# Coupon
# =============================================================================
class CouponQuerySet(QuerySet):
    pass


class Coupon(ContributorModel):
    """
    Coupon model.
    """

    objects = CouponQuerySet.as_manager()

    reward = fields.ForeignKey(
        'Reward',
        on_delete=models.CASCADE,
        help_text='The reward that coupon belong to',
    )
    kind = fields.IntegerField(
        verbose_name='Coupon kind',
        choices=CouponKindsEnum.to_tuple(),
        default=CouponKindsEnum.PERCENTAGE.value,
    )
    code = fields.CharField(
        verbose_name='Reward unique coupon code',
        max_length=10,
        unique=True,
    )
    start_date = models.DateTimeField(
        verbose_name='Valid date time',
        null=True,
        blank=True,
    )
    end_date = models.DateTimeField(
        verbose_name='Expire date time',
        null=True,
        blank=True,
    )
    amount = fields.FloatField(
        help_text='Depend on coupon kind. If coupon kind is percentage coupon, '
                  'its value must be between 0 to 100. If coupon kind is money,'
                  'its value must be greater than 0',
        validators=[MinValueValidator(0)],
    )
    target_amount = fields.FloatField(
        help_text='How much need to be bought to use coupon.',
        validators=[MinValueValidator(0)],
    )
    is_minimum_purchase = fields.BooleanField(
        default=True,
        help_text='This flag is used to determine when customer can use coupon.'
                  '`True`: Coupon can be used when total amount on bill is '
                  'greater than or equal `target amount`.'
                  '`False`: Coupon can be used when total amount on bill is'
                  'less than target amount.',
    )
    is_one_time_using = fields.BooleanField(
        default=True,
        help_text='True if coupon is allowed one time using, '
                  '`False` if it can be used all times.',
    )
    can_by_any_product = fields.BooleanField(
        default=False,
        help_text='`True`: coupon can buy any product. '
                  '`False`: coupon can buy products in the allowed list only.',
    )
    is_active = fields.BooleanField(
        default=True,
        help_text='`True` if coupon is active; otherwise, `False`.',
    )
    is_expired = fields.BooleanField(
        default=False,
        help_text='`True` if coupon is expired; otherwise, `False`.',
    )

    def __str__(self):
        return f'coupon:{self.id}'

    def save(self, **kwargs):
        if not self.code:
            self.code = uuid.uuid4()

        super().save(**kwargs)


# =============================================================================
# Gift
# =============================================================================
class GiftQuerySet(QuerySet):
    pass


class Gift(ContributorModel):
    """
    Gift model
    """
    objects = GiftQuerySet.as_manager()

    customer = fields.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
    )
    is_active = fields.BooleanField(
        default=True,
        help_text='This flag is used to determine that customer gift is active'
                  'or not. `True` is active; otherwise, `False`.'
    )

    def __str__(self):
        return f'gift:{self.id}'


# =============================================================================
# GiftItem
# =============================================================================
class GiftItemQuerySet(QuerySet):
    pass


class GiftItem(ContributorModel):
    """
    Gift Item model
    """
    objects = GiftItemQuerySet.as_manager()

    product = fields.OneToOneField(
        Product,
        on_delete=models.CASCADE,
    )
    gift = fields.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
    )
    quantity = fields.IntegerField(
        verbose_name='Number of item',
        default=0,
        validators=[MinValueValidator(0)],
    )


# =============================================================================
# Reward
# =============================================================================
class RewardQuerySet(QuerySet):
    pass


class Reward(ContributorModel):
    """
    Reward model
    """
    objects = RewardQuerySet.as_manager()

    membership = fields.OneToOneField(
        Membership,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_active = fields.BooleanField(
        default=True,
        help_text='A flag for marking that reward is active or not',
    )

    def __str__(self):
        return f'reward:{self.id}'
