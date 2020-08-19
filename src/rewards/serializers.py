from rest_framework import serializers

from rewards.models import (
    Coupon,
    Gift,
    Reward,
)


# =============================================================================
# CouponSerializer
# =============================================================================
class CouponSerializer(serializers.ModelSerializer):
    # Serializer for Coupon model.

    class Meta:
        model = Coupon
        fields = '__all__'


# =============================================================================
# GiftSerializer
# =============================================================================
class GiftSerializer(serializers.ModelSerializer):
    # Serializer for Gift model.

    class Meta:
        model = Gift
        fields = '__all__'


# =============================================================================
# RewardSerializer
# =============================================================================
class RewardSerializer(serializers.ModelSerializer):
    # Serializer for Reward model.

    class Meta:
        model = Reward
        fields = '__all__'
