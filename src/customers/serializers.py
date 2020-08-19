from rest_framework import serializers

from customers.models import (
    Customer,
    Membership,
)


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = '__all__'
        read_only_fields = ['level', ]


# =============================================================================
# CustomerSerializer
# =============================================================================
class CustomerSerializer(serializers.ModelSerializer):
    # Serializer for Customer model.

    class Meta:
        model = Customer
        fields = '__all__'
