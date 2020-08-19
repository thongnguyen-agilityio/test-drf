from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from drf_core.models import (
    ContributorModel,
    QuerySet,
)
from drf_core import fields


# =============================================================================
# MembershipLevel
# =============================================================================
class MembershipLevelQuerySet(QuerySet):
    pass


class MembershipLevel(ContributorModel):
    """
    MembershipLevel model
    """
    objects = MembershipLevelQuerySet.as_manager()

    previous = fields.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='level_previous',
        null=True,
        blank=True,
    )
    next = fields.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='level_next',
        null=True,
        blank=True,
    )
    name = fields.ShortNameField(
        null=False,
        blank=False,
        unique=True,
    )
    require_point = fields.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Require point to reach the membership level.'
    )
    earning_point_rate = fields.FloatField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='The rate to calculate the earning point for customer based'
                  'on the total amount on the bill.',
    )
    burning_point_rate = fields.FloatField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='The rate to calculate amount when customer uses point to'
                  'redeem products.',
    )


# =============================================================================
# Membership
# =============================================================================
class MembershipQuerySet(QuerySet):
    pass


class Membership(ContributorModel):
    """
    Membership model.
    """
    objects = MembershipQuerySet.as_manager()

    level = models.ForeignKey(
        MembershipLevel,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        help_text='Indicate that membership is active or not. '
                  'True if active; otherwise, False',
        default=True,
    )

    def __str__(self):
        return f'membership: {self.id}'


# =============================================================================
# Email
# =============================================================================
class EmailQuerySet(QuerySet):
    pass


class Email(ContributorModel):
    """
    Email model.
    """

    objects = EmailQuerySet.as_manager()

    email = fields.EmailField()
    is_verified = fields.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'email: {self.email}, verify: {self.is_verified}'


# =============================================================================
# Customer
# =============================================================================
class CustomerQuerySet(QuerySet):
    pass


class Customer(ContributorModel):
    """
    Customer model.
    """

    objects = CustomerQuerySet.as_manager()

    name = fields.ShortNameField(
        verbose_name='Customer name',
    )
    account = fields.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
    )
    membership = fields.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    email = models.OneToOneField(
        Email,
        on_delete=models.CASCADE,
    )
    phone_number = fields.PhoneNumberField()
    available_point = fields.IntegerField(
        help_text='Current point',
        default=0,
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
    )
    total_earned_point = fields.IntegerField(
        help_text='Total earned point from the beginning',
        default=0,
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(
        help_text='Indicate that customer is active or not. '
                  'True if active; otherwise, False',
        default=True,
    )

    def __str__(self):
        return f'customer: {self.id}'

    def clean(self):
        """
        Don't allow `total_earned_point` is less than `available_point`
        """
        if self.total_earned_point < self.available_point:
            total_earned_point_msg = '`total_earned_point` must be greater ' \
                                     'than or equal `available_point`'

            available_point_msg = '`available_point` must be less ' \
                                  'than or equal `total_earned_point`'

            raise ValidationError({
                'total_earned_point': ValidationError(
                    _(total_earned_point_msg)),
                'available_point': ValidationError(_(available_point_msg))
            })

    def save(self, **kwargs):
        """
        Save the customer information.
        Check and set membership level for customer based on the total earned
        point.
        """
        try:
            level_obj = MembershipLevel.objects.filter(
                require_point__lte=self.total_earned_point
            ).order_by('-require_point').first()

            if level_obj:
                if self.membership:
                    self.membership.level = level_obj
                    self.membership.save()
                else:
                    level_filtered = Membership.objects.filter(level=level_obj)\
                                                       .first()
                    self.membership = level_filtered if level_filtered else \
                        Membership.objects.create(level=level_obj)

            super(Customer, self).save(**kwargs)
        except Exception as e:
            raise e


# =============================================================================
# AddressBook
# =============================================================================
class AddressBookQuerySet(QuerySet):
    pass


class AddressBook(ContributorModel):
    """
    AddressBook model.
    """

    objects = AddressBookQuerySet.as_manager()

    customer = fields.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    address = fields.LongNameField()
    is_default = fields.BooleanField(
        default=False,
        help_text='This flag is used to mark which address is default address.',
    )


# =============================================================================
# AssigningPoint
# =============================================================================
class AssigningPointQuerySet(QuerySet):
    pass


class AssigningPoint(ContributorModel):
    """
    AssigningPoint model.
    """

    objects = AssigningPointQuerySet.as_manager()

    customer = fields.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    point = fields.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Assigning point which assigned to customer.'
    )
    description = fields.LongDescField()
