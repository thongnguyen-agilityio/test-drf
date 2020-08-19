from rest_framework import serializers

from orders.models import (
    Order,
    OrderItem,
    Transaction,
)


# =============================================================================
# OrderItemSerializer
# =============================================================================
class OrderItemSerializer(serializers.ModelSerializer):
    # Serializer for OrderItem model.

    class Meta:
        model = OrderItem
        fields = '__all__'


# =============================================================================
# OrderSerializer
# =============================================================================
class OrderSerializer(serializers.ModelSerializer):
    # Serializer for Order model.

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'user',
            'num_of_items',
            'total_pay_amount',
        ]


class MyOrderSerializer(serializers.ModelSerializer):
    # Serializer for Order model for the current logged in user

    class Meta:
        model = Order
        fields = [
            'status',
            'total_amount',
            'shipping_address',
            'coupon',
            'burning_point',
            'total_pay_amount',
            'num_of_items',
        ]
        read_only_fields = [
            'user',
            'num_of_items',
            'total_pay_amount',
        ]


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'user',
            'status',
            'total_amount',
            'shipping_address',
            'coupon',
            'burning_point',
            'total_pay_amount',
            'num_of_items',
        ]
        read_only_fields = [
            'user',
            'num_of_items',
            'total_pay_amount',
        ]


# =============================================================================
# CartItemSerializer
# =============================================================================
class CartItemSerializer(serializers.ModelSerializer):
    # Serializer for Cart item.

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
        ]


# =============================================================================
# UpdatingCartItemSerializer
# =============================================================================
class UpdatingCartItemSerializer(serializers.ModelSerializer):
    # Serializer for updating a cart item

    class Meta:
        model = OrderItem
        fields = [
            'quantity',
        ]


# =============================================================================
# TransactionSerializer
# =============================================================================
class TransactionSerializer(serializers.ModelSerializer):
    # Serializer for Transaction model.

    class Meta:
        model = Transaction
        fields = '__all__'
