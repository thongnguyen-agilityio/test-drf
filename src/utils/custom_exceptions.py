from rest_framework import status


class BaseCustomException(Exception):
    # The HTTP status code
    status_code = None

    # The custom error code
    default_code = None

    # The developer message about the error
    default_dev_msg = None

    # The friendly user message about the error
    default_user_message = None

    # A flag to determine this error will be sent back in response data or not.
    is_an_error_response = True

    def __init__(self, developer_message=None, user_message=None, code=None):
        Exception.__init__(self)

        self.developer_message = developer_message
        self.user_message = user_message
        self.code = code

        if not developer_message:
            self.developer_message = self.default_dev_msg \
                if self.default_dev_msg else self.who_am_i()

        if not user_message:
            self.user_message = self.default_user_message \
                if self.default_user_message else self.who_am_i()

        self.code = code if code else self.default_code

    def who_am_i(self):
        return type(self).__name__

    def to_dict(self):
        return {
            'developer_message': self.developer_message,
            'user_message': self.user_message,
            'error_code': self.code
        }


# ------------------------------------------------------------------------------
# Cart Exceptions
# ------------------------------------------------------------------------------
class DuplicateCartItemException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 1001
    default_dev_msg = 'May be data body is not right or duplicate cart item'
    default_user_message = 'Cannot add product to cart. Please try again!'


class CartItemDoesNotExistException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 1002
    default_dev_msg = 'Cart item or product is not existed.'
    default_user_message = 'Cannot update this product.'


class EmptyCartException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 1003
    default_dev_msg = 'Only one cart for each user. Empty or null cart ' \
                      'cannot be checkout.'
    default_user_message = 'Sorry, you cannot checkout the cart.'


# ------------------------------------------------------------------------------
# Order Exceptions
# ------------------------------------------------------------------------------
class OrderNotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 2001
    default_dev_msg = 'Order not found.'
    default_user_message = 'This order is not available.'


class CancelOrderDeniedException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 2002
    default_dev_msg = 'Something wrong. Only “Waiting” status order can be ' \
                      'canceled.'
    default_user_message = 'This order is in-progress. You cannot cancel. ' \
                           'Please contact the supporter if for more info!'


class PayOrderDeniedException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 2003
    default_dev_msg = 'Only `IN-PROGRESS` or `SHIPPING` order can be paid'
    default_user_message = 'Cannot pay this order'


# ------------------------------------------------------------------------------
# Coupon Exceptions
# ------------------------------------------------------------------------------
class InvalidCouponException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 3001
    default_dev_msg = 'Coupon code is not valid.'
    default_user_message = 'Coupon code is not valid (the promotion campaign ' \
                           'does not exist).'


# ------------------------------------------------------------------------------
# Category Exceptions
# ------------------------------------------------------------------------------
class CategoryDuplicatedException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 4001
    default_dev_msg = 'Duplicate category.'
    default_user_message = 'Duplicate category.'


class CategoryNotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 4002
    default_dev_msg = 'Category not found.'
    default_user_message = 'Category not found.'


# ------------------------------------------------------------------------------
# Customer Exceptions
# ------------------------------------------------------------------------------
class CustomerNotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 5001
    default_dev_msg = 'Customer not found.'
    default_user_message = 'Customer not found.'


# ------------------------------------------------------------------------------
# Point Exceptions
# ------------------------------------------------------------------------------
class NotEnoughPointsException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 6001
    default_dev_msg = 'Not enough points.'
    default_user_message = 'Not enough points.'


# ------------------------------------------------------------------------------
# Product Exceptions
# ------------------------------------------------------------------------------
class ProductNotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 7001
    default_dev_msg = 'Product not found.'
    default_user_message = 'Product not found.'


class InvalidBodyDataException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 8400
    default_dev_msg = 'Invalid body data.'
    default_user_message = 'Invalid body data.'
