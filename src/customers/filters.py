from drf_core.filtering import BaseFiltering
from customers.models import (
    Customer,
    Membership,
)


# =============================================================================
# Customer
# =============================================================================
class CustomerFiltering(BaseFiltering):

    class Meta:
        model = Customer
        exclude = []


# =============================================================================
# Membership
# =============================================================================
class MembershipFiltering(BaseFiltering):

    class Meta:
        model = Membership
        exclude = []
