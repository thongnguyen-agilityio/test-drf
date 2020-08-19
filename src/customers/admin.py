from django.contrib import admin
from drf_core.admin import BaseModelAdmin

from customers.models import (
    Customer,
    Membership,
)


# =============================================================================
# Customer
# =============================================================================
@admin.register(Customer)
class CustomerAdmin(BaseModelAdmin):
    pass


# =============================================================================
# Membership
# =============================================================================
@admin.register(Membership)
class MembershipAdmin(BaseModelAdmin):
    pass
