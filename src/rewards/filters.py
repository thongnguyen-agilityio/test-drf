from drf_core.filtering import BaseFiltering

from rewards.models import (
    Coupon,
    Gift,
    Reward,
)


# =============================================================================
# Coupon
# =============================================================================
class CouponFiltering(BaseFiltering):

    class Meta:
        model = Coupon
        exclude = []


# =============================================================================
# Gift
# =============================================================================
class GiftFiltering(BaseFiltering):

    class Meta:
        model = Gift
        exclude = []


# =============================================================================
# Reward
# =============================================================================
class RewardFiltering(BaseFiltering):

    class Meta:
        model = Reward
        exclude = []
