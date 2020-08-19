from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from drf_core.models import (
    ContributorModel,
    QuerySet,
)
from drf_core import fields
from app.constants import OrderStatusesEnum
from products.models import Product
from rewards.models import Coupon
from customers.models import Customer, AddressBook


# =============================================================================
# Order
# =============================================================================
class OrderQuerySet(QuerySet):
    pass


class Order(ContributorModel):
    """
    Order model
    """
    objects = OrderQuerySet.as_manager()
    user = fields.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        help_text='The owner of the order',
    )
    status = fields.IntegerField(
        choices=OrderStatusesEnum.to_tuple(),
        default=OrderStatusesEnum.SHOPPING.value,
        help_text='The order status',
    )
    total_amount = fields.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Total amount before applying coupon and points',
    )
    shipping_address = fields.ForeignKey(
        AddressBook,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        help_text='The shipping address',
    )
    coupon = fields.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        help_text='The coupon',
    )
    burning_point = fields.IntegerField(
        default=0,
        help_text='Number of points which used to redeem products',
    )

    @property
    def total_pay_amount(self) -> float:
        """
        Calculate the total payment amount

        @return: Total payment amount
        """
        if self.burning_point:
            customer_obj = Customer.objects.get(account=self.user)
            burning_point_rate = customer_obj.membership.level.\
                burning_point_rate

            return self.total_amount - burning_point_rate * self.burning_point

        else:
            return self.total_amount

    @property
    def num_of_items(self) -> int:
        """
        Number of items in the cart

        @return: The number of order/cart items
        """
        return OrderItem.objects.non_archived_only().\
            filter(order=self.id).count()

    def __str__(self):
        return f'order-{self.id}'

    def clean(self):
        """
        Don't allow `total_pay_amount` greater than `total_amount`
        """
        if self.total_amount < self.total_pay_amount:
            total_amount_msg = '`total_amount` must be greater ' \
                               'than or equal `total_pay_amount`'

            total_pay_amount_msg = '`total_pay_amount` must be less ' \
                                   'than or equal `total_amount`'

            raise ValidationError({
                'total_pay_amount': ValidationError(
                    _(total_pay_amount_msg)),
                'total_amount': ValidationError(_(total_amount_msg))
            })

    def save(self, **kwargs):
        """
        Save an order and auto create transaction based on the order status.
        If order is paid, transaction is created if not existed.
        Otherwise, just save order only

        TODO: Need to calculate total pay amount when applying coupon.
            Temporary skip this task.
        """
        try:
            # If order status is not paid status. Just save and by pass.
            if self.status is not OrderStatusesEnum.PAID.value:
                super(Order, self).save(**kwargs)
                return

            self._create_transaction(**kwargs)
        except Exception as e:
            raise e

    def _create_transaction(self, **kwargs):
        """
        Auto create a transaction if the order status is paid
        """
        # Get customer info who has this order
        membership_level = None
        customer_obj = Customer.objects.get(account=self.user)
        if customer_obj and customer_obj.membership:
            membership_level = customer_obj.membership.level

        earning_point_rate = membership_level.earning_point_rate \
            if membership_level else 0

        earning_point = int(self.total_pay_amount * earning_point_rate)

        transaction_data = {
            'order': self,
            'user': self.user,
            'total_amount': self.total_amount,
            'total_pay_amount': self.total_pay_amount,
            'earning_point': earning_point,
            'created_by': self.last_modified_by,
            'last_modified_by': self.last_modified_by,
        }

        # Update earning point for customer.
        customer_obj.total_earned_point += earning_point
        customer_obj.available_point += earning_point
        customer_obj.save()

        # If order status is paid status, check and create transaction.
        if self.pk is None:
            super(Order, self).save(**kwargs)
            Transaction.objects.create(**transaction_data)
        else:
            old_instance = Order.objects.get(pk=self.pk)
            super(Order, self).save(**kwargs)

            transaction = Transaction.objects.filter(order=self)

            if old_instance.status is not OrderStatusesEnum.PAID.value \
                    and len(transaction) == 0:
                Transaction.objects.create(**transaction_data)


# =============================================================================
# OrderItem
# =============================================================================
class OrderItemQuerySet(QuerySet):
    pass


class OrderItem(ContributorModel):
    """
    Order Item model
    """
    objects = OrderItemQuerySet.as_manager()
    order = fields.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = fields.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = fields.IntegerField(
        validators=[MinValueValidator(1)],
    )
    copy_price = fields.FloatField(
        default=0,
        null=True,
    )

    @property
    def price(self):
        if not self.copy_price:
            self.copy_price = self.product.price

        return self.copy_price

    @property
    def amount(self):
        return self.price * self.quantity

    def __str__(self):
        return f'order-item-{self.id}'

    def delete(self, using=None, keep_parents=False):
        """
        Delete an order item and update the order information.
        """
        try:
            super(OrderItem, self).delete(using, keep_parents)

            self.order.total_amount = models.F('total_amount') - self.amount
            self.order.save()
        except Exception as e:
            raise e

    def save(self, **kwargs):
        """
        Save an order item and update the order information.
        """
        try:
            if self.pk is None:
                super(OrderItem, self).save(**kwargs)
                self.order.total_amount += self.amount
                self.order.save()

            else:
                old_order_item = OrderItem.objects.get(pk=self.pk)
                super(OrderItem, self).save(**kwargs)
                if old_order_item.amount is not self.amount:
                    self.order.total_amount = self.order.total_amount - \
                                              old_order_item.amount + \
                                              self.amount
                    self.order.save()
        except Exception as e:
            raise e


# =============================================================================
# Transaction
# =============================================================================
class TransactionQuerySet(QuerySet):
    pass


class Transaction(ContributorModel):
    """
    Transaction model
    """
    objects = TransactionQuerySet.as_manager()

    order = fields.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        help_text='The order which transaction belong to',
    )
    user = fields.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        help_text='The user who own this transaction',
    )
    coupon = fields.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    total_amount = fields.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Total amount of an order',
    )
    total_pay_amount = fields.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='The actual amount that customer need to pay',
    )
    earning_point = fields.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        help_text='Number of point of an order that customer earns',
    )
    burning_point = fields.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        help_text='Number of point that customer spend to redeem product',
    )
