from django.db.models import F
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from drf_core import apis

from rewards.models import Coupon
from utils.custom_exceptions import (
    DuplicateCartItemException,
    CartItemDoesNotExistException,
    EmptyCartException,
    InvalidCouponException,
    InvalidBodyDataException,
)
from app.constants import OrderStatusesEnum
from customers.models import AddressBook
from orders.models import (
    Order,
    OrderItem,
)
from orders.serializers import (
    OrderItemSerializer,
    CartItemSerializer,
    UpdatingCartItemSerializer,
    CartSerializer,
)
from products.models import Product


class CartBaseViewSet(apis.BaseEmptyViewSet, apis.AuthenticationViewSet):
    queryset = Order.objects.non_archived_only()
    serializer_class = CartSerializer

    cart = None

    @classmethod
    def get_cart(cls, user):
        is_cart_available = cls.cart is not None and \
                            cls.cart.status == OrderStatusesEnum.SHOPPING
        if is_cart_available:
            return cls.cart

        shopping_status = OrderStatusesEnum.SHOPPING.value
        carts = cls.queryset.filter(status=shopping_status)
        if len(carts) > 1:
            raise ValueError('There are multiple shopping cart in system. '
                             'Please make sure only one cart exists.')

        cls.cart = carts.first() if carts else cls._create_cart(user)
        return cls.cart

    @classmethod
    def get_cart_items(cls, cart):
        if not cart:
            return []

        cart_items = OrderItem.objects.non_archived_only().filter(order=cart)
        return cart_items

    @classmethod
    def _create_cart(cls, user):
        order_data = {
            'status': OrderStatusesEnum.SHOPPING.value,
            'user': user
        }

        return Order.objects.create(**order_data)

    @classmethod
    def change_cart_item(cls, cart_obj, product_item, is_added_to_cart):
        """
        Change the cart item

        - Add more existed product to cart.
        - Add new product to cart.
        - Update product item quantity in cart.

        @param is_added_to_cart: A flag to determine add to cart or not
        @param cart_obj: Shopping cart object
        @param product_item: Product item data
        @return: Return `True` if the process completed successfully.
        """
        try:
            cart_item_objs = OrderItem.objects.non_archived_only() \
                .filter(order=cart_obj, product=product_item['product'])
        except EmptyCartException as e:
            raise e

        is_duplicated_item = len(cart_item_objs) > 1
        is_one_item = len(cart_item_objs) == 1

        # Do not allow duplicate cart item.
        if is_duplicated_item:
            raise DuplicateCartItemException('There are duplicate product item '
                                             'in the cart')

        if is_added_to_cart:
            if is_one_item:
                cart_item_objs.update(quantity=F('quantity') + 1)
            else:
                # There is no item in the cart. Create a new one.
                new_item_values = {
                    'order': cart_obj,
                    'product': Product.objects.get(pk=product_item['product']),
                    'quantity': 1
                }

                cart_item_obj = OrderItem(**new_item_values)
                cart_item_obj.save()

            return True
        else:
            # Update cart item quantity
            if is_one_item:
                updated_data = {
                    'quantity': product_item.get('quantity', None)
                }

                UpdatingCartItemSerializer(data=updated_data).is_valid(
                    raise_exception=True
                )

                cart_item_objs.update(**updated_data)
                return True
            else:
                raise CartItemDoesNotExistException('Cart item not found')


class CartViewSet(CartBaseViewSet):
    """
    It helps to provide APIs to work with the cart of the current logged in
    user. Here are some objectives

    - Add new product to the cart
    - Checkout a shopping cart
    - Get list of items in a cart
    - Add shipping address to the cart
    """
    resource_name = 'cart/me'

    def create(self, request, *args, **kwargs):
        """
        Add product to cart.

        Create new or increase product quantity if cart item is already exists
        """
        user_obj = request.user
        buying_item = request.data

        cart_obj = self.get_cart(user_obj)
        CartItemSerializer(data=buying_item).is_valid(raise_exception=True)
        self.change_cart_item(cart_obj, buying_item, is_added_to_cart=True)

        return self.create_response_success()

    @action(
        methods=['PUT'],
        detail=False
    )
    def checkout(self, request):
        """
        Checkout a shopping cart to create an order.
        """
        user = request.user
        cart = self.get_cart(user)
        cart_items = self.get_cart_items(cart)
        is_not_empty_cart = len(cart_items) > 0

        if is_not_empty_cart:
            cart.status = OrderStatusesEnum.WAITING.value
            cart.save()

            return self.create_response(data={'order_id': cart.id})
        else:
            raise EmptyCartException()

    @action(
        methods=['GET'],
        detail=False
    )
    def items(self, request):
        """
        Get shopping cart items.
        """
        cart_obj = self.get_cart(request.user)
        if not cart_obj:
            return self.create_response(data=[])

        queryset = self.get_cart_items(cart_obj)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderItemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderItemSerializer(queryset, many=True)
        return self.create_response(data=serializer.data)

    @action(
        methods=['GET'],
        detail=False,
    )
    def overview(self, request):
        """
        Get the overview of the cart.
        """
        cart_obj = self.get_cart(request.user)
        response_data = {
            'count': cart_obj.num_of_items,
            'total_amount': cart_obj.total_amount,
            'total_pay_amount': cart_obj.total_pay_amount
        }
        return self.create_response(data=response_data)

    @action(
        methods=['PUT'],
        detail=False,
    )
    def redeeming_by_points(self, request, **kwargs):
        """
        Use point to redeem products
        """
        data = request.data
        user_obj = request.user

        cart_obj = self.get_cart(user_obj)
        is_empty_cart = not len(self.get_cart_items(cart_obj))
        if is_empty_cart:
            raise EmptyCartException()

        points = data.get('points', None)
        is_not_valid_points = type(points) is not int or \
            points <= 0 or points > user_obj.customer.available_point

        if is_not_valid_points:
            raise InvalidBodyDataException()

        cart_obj.points = points
        cart_obj.save()

        return self.create_response_success()


class CartAddressViewSet(CartBaseViewSet):
    """
    Provides APIs to set shipping address to an existing cart
    """
    resource_name = 'cart/me/shipping_address'

    def update(self, request, **kwargs):
        """
        Add shipping address to an existing cart
        """
        cart_obj = self.get_cart(request.user)
        address_id = kwargs.get('pk')

        address_obj = get_object_or_404(AddressBook, pk=address_id)
        cart_obj.shipping_address = address_obj
        cart_obj.save()
        return self.create_response_success()


class CartCouponViewSet(CartBaseViewSet):
    """
    Provides APIs to set coupon to the cart
    """
    resource_name = 'cart/me/coupons'

    def update(self, request, **kwargs):
        """
        Add coupon to the cart

        TODO: Need to update the save method of order model to calculate the
              total amount for the cart after applying coupon.
              Temporarily keep the code as is to train API design only.
        """
        coupon_code = kwargs.get('pk', None)
        user_obj = request.user
        try:
            coupon_obj = Coupon.objects.non_archived_only()\
                .get(code=coupon_code)
        except Exception:
            raise InvalidCouponException()

        cart_obj = self.get_cart(user_obj)
        cart_item_objs = self.get_cart_items(cart_obj)
        is_empty_cart = not len(cart_item_objs)
        if is_empty_cart:
            raise EmptyCartException()

        cart_obj.coupon = coupon_obj
        cart_obj.save()

        return self.create_response_success()


class CartItemViewSet(CartBaseViewSet):
    """
    It helps to provide APIs to work with individual cart item. Here are some
    objectives

    - Update shopping cart item quantity
    - Remove a shopping cart item
    """
    serializer_class = CartItemSerializer

    resource_name = 'cart/me/items'

    def update(self, request, **kwargs):
        """
        Increase/decrease number of product items in the cart.
        """
        user_obj = request.user
        cart_obj = self.get_cart(user_obj)
        product_id = kwargs.get('pk')
        updated_data = request.data
        updated_data['product'] = product_id

        # Verify cart item before update
        CartItemSerializer(data=updated_data).is_valid(raise_exception=True)
        self.change_cart_item(cart_obj, updated_data, is_added_to_cart=False)
        return self.create_response_success()

    def destroy(self, request, **kwargs):
        """
        Remove product item from the cart.
        """
        product_id = kwargs.get('pk')
        user_obj = request.user
        cart_obj = self.get_cart(user_obj)

        try:
            cart_item_obj = OrderItem.objects.get(product=product_id,
                                                  order=cart_obj)
            cart_item_obj.delete()
            return self.create_non_content_response()
        except Exception:
            raise CartItemDoesNotExistException(
                developer_message='Maybe not exist cart or product',
                user_message='Cannot delete this product'
            )


apps = [
    CartViewSet,
    CartAddressViewSet,
    CartCouponViewSet,
    CartItemViewSet,
]
