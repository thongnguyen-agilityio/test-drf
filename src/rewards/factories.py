import pytz

from drf_core import factories

from accounts.factories import UserFactory
from app.constants import CouponKindsEnum
from rewards.models import (
    Coupon,
    Gift,
    Reward,
)
from customers.factories import MembershipFactory

utc = pytz.UTC


# =============================================================================
# Gift
# =============================================================================
class GiftFactory(factories.ModelFactory):
    # Factory data for Gift model.

    @factories.lazy_attribute
    def customer(self):
        return UserFactory().customer

    class Meta:
        model = Gift
        django_get_or_create = (
            'customer',
        )


# =============================================================================
# Reward
# =============================================================================
class RewardFactory(factories.ModelFactory):
    # Factory data for Reward model.

    membership = factories.SubFactory(MembershipFactory)
    is_active = factories.FuzzyChoice([True, False])

    class Meta:
        model = Reward
        django_get_or_create = (
            'membership',
            'is_active',
        )


# =============================================================================
# Coupon
# =============================================================================
class CouponFactory(factories.ModelFactory):
    # Factory data for Coupon model.
    reward = factories.SubFactory(RewardFactory)
    kind = factories.FuzzyChoice(CouponKindsEnum.values())
    amount = factories.FuzzyInteger(10, 100)
    target_amount = factories.FuzzyInteger(300, 500)
    is_minimum_purchase = factories.FuzzyChoice([True, False])

    class Meta:
        model = Coupon
        django_get_or_create = (
            'reward',
            'kind',
            'amount',
            'target_amount',
            'is_minimum_purchase',
        )
