from core.apis import BaseViewSet
from customers.models import (
    Customer,
    Membership,
)
from customers.serializers import (
    CustomerSerializer,
    MembershipSerializer,
)
from customers.filters import (
    CustomerFiltering,
    MembershipFiltering,
)


# =============================================================================
# Membership
# =============================================================================
class MembershipViewSet(BaseViewSet):
    # Membership ViewSet

    queryset = Membership.objects.non_archived_only()
    serializer_class = MembershipSerializer
    filter_class = MembershipFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'memberships'


# =============================================================================
# Customer
# =============================================================================
class CustomerViewSet(BaseViewSet):
    # Customer ViewSet

    queryset = Customer.objects.non_archived_only()
    serializer_class = CustomerSerializer
    filter_class = CustomerFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'customers'


apps = [
    CustomerViewSet,
]
