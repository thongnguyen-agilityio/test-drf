from core.apis import BaseViewSet
from rewards.models import (
    Coupon,
    Gift,
    Reward,
)
from rewards.serializers import (
    CouponSerializer,
    GiftSerializer,
    RewardSerializer,
)
from rewards.filters import (
    CouponFiltering,
    GiftFiltering,
    RewardFiltering,
)


# =============================================================================
# Coupon
# =============================================================================
class CouponViewSet(BaseViewSet):
    # Coupon ViewSet

    queryset = Coupon.objects.non_archived_only()
    serializer_class = CouponSerializer
    filter_class = CouponFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'coupons'


# =============================================================================
# Gift
# =============================================================================
class GiftViewSet(BaseViewSet):
    # Gift ViewSet

    queryset = Gift.objects.non_archived_only()
    serializer_class = GiftSerializer
    filter_class = GiftFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'gifts'


# =============================================================================
# Reward
# =============================================================================
class RewardViewSet(BaseViewSet):
    # Reward ViewSet

    queryset = Reward.objects.non_archived_only()
    serializer_class = RewardSerializer
    filter_class = RewardFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'rewards'


apps = [
    CouponViewSet,
    GiftViewSet,
    RewardViewSet,
]
