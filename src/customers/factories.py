from drf_core import factories

from customers.models import (
    Membership,
    MembershipLevel,
    Email,
    AddressBook,
)
from debugging.management.commands.initmembershiplevels import Command


# =============================================================================
# Email
# =============================================================================
class EmailFactory(factories.ModelFactory):
    # Factory data for Membership model.

    email = factories.Faker('email')
    is_verified = factories.FuzzyChoice([True, False])

    class Meta:
        model = Email
        django_get_or_create = (
            'email',
            'is_verified',
        )


# =============================================================================
# MembershipLevel
# =============================================================================
class MembershipLevelFactory(factories.ModelFactory):
    """
    Factory data for MembershipLevel model.
    """
    previous = None
    name = factories.FuzzyText()
    require_point = 0
    earning_point_rate = 1
    burning_point_rate = 1

    class Meta:
        model = MembershipLevel
        django_get_or_create = (
            'previous',
            'name',
            'require_point',
            'earning_point_rate',
            'burning_point_rate',
        )


# =============================================================================
# Membership
# =============================================================================
class MembershipFactory(factories.ModelFactory):
    # Factory data for Membership model.

    is_active = True

    @factories.lazy_attribute
    def level(self):
        # Init membership level
        Command.handle(None)

        levels = MembershipLevel.objects.all()
        return factories.FuzzyChoice(levels).fuzz()

    class Meta:
        model = Membership
        django_get_or_create = (
            'level',
            'is_active',
        )


class AddressBookFactory(factories.ModelFactory):
    """
    Factory customer address
    """
    address = factories.Faker('address')

    class Meta:
        model = AddressBook
        django_get_or_create = (
            'customer',
        )
