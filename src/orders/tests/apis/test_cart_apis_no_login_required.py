from drf_core.tests import BaseTestCase

from orders.factories import (
    CartFactory,
    CartItemFactory,
)
from orders.models import (
    Order,
    OrderItem,
)
from orders.apis.cart import (
    CartViewSet,
    CartAddressViewSet,
    CartItemViewSet,
)
from products.models import Product
from rewards.factories import CouponFactory
from rewards.models import Coupon


class CartViewSetTestCase(BaseTestCase):
    """
    Test for cart APIs /api/v1/cart/me/
    """
    resource = CartViewSet

    def setUp(self) -> None:
        super().setUp()
        self.auth = None

    def tearDown(self) -> None:
        super(CartViewSetTestCase, self).tearDown()
        Coupon.objects.all().delete()

    # ==========================================================================
    # API should be forbidden if user is not logged in.
    # ==========================================================================
    def test_get_my_cart_forbidden(self):
        """
        Test API GET /api/v1/cart/me/
        """
        self.get_json_method_forbidden()

    def test_get_my_cart_items_forbidden(self):
        """
        Test API GET /api/v1/cart/me/items/
        """
        self.get_json_method_forbidden('items/')

    def test_checkout_cart_forbidden(self):
        """
        Test API PUT /api/v1/cart/me/checkout/
        """
        self.put_json_method_forbidden('checkout/')

    def test_post_add_a_product_to_cart_forbidden(self):
        """
        Test API POST /api/v1/cart/me/
        """
        self.post_json_method_forbidden(data={})

    def test_get_cart_overview_forbidden(self):
        """
        Test get cart overview forbidden

        API: GET /api/v1/cart/me/overview/
        """
        self.get_json_method_forbidden(fragment='overview/')

    def test_put_redeeming_products_by_points_forbidden(self):
        """
        Test put redeeming products by points forbidden

        API: GET /api/v1/cart/me/redeeming_by_points/
        """
        self.put_json_method_forbidden(fragment='redeeming_by_points/', data={})

    def test_put_add_coupon_to_cart_forbidden(self):
        coupon_obj = CouponFactory()
        self.put_json_method_forbidden(
            fragment=f'coupons/{coupon_obj.code}/',
            data={}
        )


class CartAddressViewSetTestCase(BaseTestCase):
    """
    Test for cart's address APIs /api/v1/cart/me/shipping_address/
    """
    resource = CartAddressViewSet

    def setUp(self) -> None:
        super().setUp()
        self.auth = None

    def tearDown(self) -> None:
        super(CartAddressViewSetTestCase, self).tearDown()

    def test_put_add_shipping_address_forbidden(self):
        """
        Test API PUT /api/v1/cart/me/shipping_address/
        """
        self.put_json_method_forbidden(data={})


class CartItemViewSetTestCase(BaseTestCase):
    """
    Test for cart's address APIs /api/v1/cart/me/items/
    """
    resource = CartItemViewSet

    def setUp(self) -> None:
        super().setUp()
        # Create a cart for testing
        self.auth = None

    def tearDown(self) -> None:
        Order.objects.all().delete()
        Product.objects.all().delete()
        OrderItem.objects.all().delete()

    def test_put_update_cart_item_forbidden(self):
        # Create a cart for testing
        cart_obj = CartFactory()
        cart_item = CartItemFactory(order=cart_obj)

        self.put_json_method_forbidden(data={},
                                       fragment=f'{cart_item.product}/')

    def test_delete_cart_item_forbidden(self):
        cart_obj = CartFactory()
        cart_item = CartItemFactory(order=cart_obj)

        self.delete_method_forbidden(data={},
                                     fragment=f'{cart_item.product}/')
