from typing import Tuple, List

from rest_framework import status
from drf_core import factories

from app.constants import OrderStatusesEnum
from accounts.factories import UserFactory
from core.tests.base import BaseViewSetTestCase
from customers.factories import AddressBookFactory
from customers.models import AddressBook
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
from products.factories import ProductFactory
from products.models import Product
from rewards.factories import CouponFactory


class CartBaseTestCase(BaseViewSetTestCase):

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        Product.objects.all().delete()

    @classmethod
    def generate_cart_and_its_items(cls, num_of_items: int = 2) \
            -> Tuple[Order, List[OrderItem]]:
        # Clean data
        Order.objects.filter(status=OrderStatusesEnum.SHOPPING.value).delete()

        cart_obj = CartFactory()
        cart_item_objs = [CartItemFactory(order=cart_obj)
                          for _ in range(num_of_items)]
        return cart_obj, cart_item_objs


class CartViewSetTestCase(CartBaseTestCase):
    """
    Test for cart APIs /api/v1/cart/me/
    """
    resource = CartViewSet

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def _test_add_product_to_cart(self) -> None:
        """
        Helper method to test adding product to cart.
        """
        product_obj = ProductFactory()
        data = {
            'product': product_obj.id,
            'quantity': factories.FuzzyInteger(1, 10).fuzz()
        }

        resp = self.post_json(data=data)
        resp_data = resp.data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data['success'], True)

    # --------------------------------------------------------------------------
    # Test success
    # --------------------------------------------------------------------------
    def test_post_add_a_product_item_to_cart_ok(self) -> None:
        """
        Test add a product to cart.
        """
        self._test_add_product_to_cart()

        # Re-add product to cart and test
        self._test_add_product_to_cart()

    def test_get_list_cart_items_ok(self) -> None:
        # Get empty cart items

        Order.objects.all().delete()
        resp = self.get_json(fragment='items/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

        # Get list of cart items
        cart_obj, cart_item_objs = self.generate_cart_and_its_items()
        resp = self.get_json(fragment='items/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(cart_item_objs))

    def test_put_checkout_cart_ok(self) -> None:
        """
        Test checking out a cart successfully.
        """
        cart_obj, cart_item_objs = self.generate_cart_and_its_items()
        resp = self.put_json(fragment='checkout/', data={})
        resp_data = resp.data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data['order_id'], cart_obj.id)

    # --------------------------------------------------------------------------
    # Test bad request
    # --------------------------------------------------------------------------
    def test_post_add_to_cart_attribute_error_bad_request(self):
        product_obj = ProductFactory()
        data = {
            'wrong_product': product_obj.id,
            'quantity': factories.FuzzyInteger(1, 10).fuzz()
        }

        response = self.post_json(data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.has_attribute_errors(response)

    def test_put_checkout_cart_bad_request(self) -> None:
        cart_obj, _ = self.generate_cart_and_its_items(0)
        resp = self.put_json(fragment='checkout/', data={})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Test error response
        self.has_valid_custom_error_response(resp)

    def test_get_cart_overview_ok(self) -> None:
        """
        Test get cart overview

        API: GET /api/v1/cart/me/overview/
        """
        cart_obj, _ = self.generate_cart_and_its_items(2)
        resp = self.get_json(fragment='overview/', data={})
        data = resp.data

        self.assertHttpOK(resp)
        self.assertEqual(data['count'], 2)
        self.assertGreaterEqual(data['total_amount'], 0)
        self.assertGreaterEqual(data['total_pay_amount'], 0)

    def test_put_redeeming_products_by_points_ok(self):
        """
        Test redeem products by points ok

        API PUT /api/v1/cart/me/redeeming_by_points/
        """
        # Create cart
        cart_obj, _ = self.generate_cart_and_its_items(2)

        # Add points to user for test.
        customer_obj = self.authenticated_user.customer
        customer_obj.available_point = 100
        customer_obj.save()

        # Test API
        request_data = {
            'points': 10
        }

        resp = self.put_json(fragment='redeeming_by_points/', data=request_data)
        self.assertHttpOK(resp)
        self.assertEqual(resp.data['success'], True)

    def test_put_redeeming_products_by_points_bad_request(self):
        """
        Test redeem products by points bad request

        API PUT /api/v1/cart/me/redeeming_by_points/
        """
        # Create cart
        cart_obj, _ = self.generate_cart_and_its_items(2)

        customer_obj = self.authenticated_user.customer

        # Use more than available points to redeem products
        request_data = {
            'points': customer_obj.available_point + 1
        }

        resp = self.put_json(fragment='redeeming_by_points/', data=request_data)
        self.assertHttpBadRequest(resp)
        self.has_valid_custom_error_response(resp)

        # Use more negative points to redeem products
        request_data = {
            'points': -1
        }

        resp = self.put_json(fragment='redeeming_by_points/', data=request_data)
        self.assertHttpBadRequest(resp)
        self.has_valid_custom_error_response(resp)

        # Send not valid data request
        request_data = {
            'test': -1
        }

        resp = self.put_json(fragment='redeeming_by_points/', data=request_data)
        self.assertHttpBadRequest(resp)
        self.has_valid_custom_error_response(resp)

    def test_put_add_coupon_to_cart_ok(self):
        """
        Test adding coupon to cart ok

        API PUT /api/v1/cart/me/coupons/{coupon_code}/
        """
        # Generate cart
        self.generate_cart_and_its_items()

        # Create a coupon
        coupon_obj = CouponFactory()
        fragment = f'coupons/{coupon_obj.code}/'
        resp = self.put_json(fragment=fragment, data={})
        self.assertHttpOK(resp)
        self.assertEqual(resp.data['success'], True)

    def test_put_add_coupon_to_cart_bad_request(self):
        # Create a coupon
        coupon_obj = CouponFactory()

        # Test adding valid coupon to empty cart.

        # Generate cart with no items
        self.generate_cart_and_its_items(0)

        fragment = f'coupons/{coupon_obj.code}/'
        resp = self.put_json_bad_request(fragment=fragment, data={})
        self.assertHttpBadRequest(resp)
        self.has_valid_custom_error_response(resp)

        # Test adding invalid coupon to non empty cart.

        # Generate cart with no items
        self.generate_cart_and_its_items(0)
        fragment = f'coupons/{coupon_obj.code}/'
        resp = self.put_json_bad_request(fragment=fragment, data={})
        self.assertHttpBadRequest(resp)
        self.has_valid_custom_error_response(resp)


class CartAddressViewSetTestCase(CartBaseTestCase):
    """
    Test for cart APIs /api/v1/cart/me/shipping_address/
    """
    resource = CartAddressViewSet

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        AddressBook.objects.all().delete()

    # --------------------------------------------------------------------------
    # Test success
    # --------------------------------------------------------------------------
    def test_put_add_shipping_address_to_cart_ok(self):
        # Create an address object
        user_obj = UserFactory()
        address_obj = AddressBookFactory(customer=user_obj.customer)

        # Create a valid shopping cart
        self.generate_cart_and_its_items()

        # Testing
        resp = self.put_json(data={}, fragment=f'{address_obj.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data.get('success'))

    # --------------------------------------------------------------------------
    # Test bad request
    # --------------------------------------------------------------------------
    def test_put_add_shipping_address_to_cart_not_found(self):
        wrong_address_id = factories.Faker('uuid4').generate()
        resp = self.put_json(data={}, fragment=f'{wrong_address_id}/')
        print(resp.__dict__)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.has_attribute_errors(resp)


class CartItemsViewSetTestCase(CartBaseTestCase):
    """
    Test for cart APIs /api/v1/cart/me/items/
    """
    resource = CartItemViewSet

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_put_update_cart_item_quantity_ok(self):
        data = {'quantity': 5}
        _, cart_item_objs = self.generate_cart_and_its_items()
        resp = self.put_json(data=data,
                             fragment=f'{cart_item_objs[0].product.id}/')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data.get('success'))

    def test_put_update_cart_item_quantity_bad_request(self):
        # Try to update a not existing item
        data = {'quantity': 5}
        wrong_product_id = factories.Faker('uuid4').generate()
        resp = self.put_json(data=data, fragment=f'{wrong_product_id}/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.has_attribute_errors(resp)

    def test_delete_cart_item_ok(self):
        # Create a cart for testing
        _, cart_item_objs = self.generate_cart_and_its_items()
        resp = self.delete_json(data={},
                                fragment=f'{cart_item_objs[0].product.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_cart_item_bad_request(self):
        _, cart_item_objs = self.generate_cart_and_its_items()
        wrong_product_id = factories.Faker('uuid4').generate()
        resp = self.delete_json(data={}, fragment=f'{wrong_product_id}/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.has_valid_custom_error_response(resp)
