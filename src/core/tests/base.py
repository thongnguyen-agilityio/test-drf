from requests import Response
from drf_core.tests import BaseTestCase


class BaseViewSetTestCase(BaseTestCase):
    resource = None

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def has_attribute_errors(self, response: Response) -> None:
        """
        Test attribute errors to make sure the attribute error response has
        right data format.

        @param response: Response data
        """
        response_data = response.data
        self.assertTrue('errors' in response_data.keys())

    def has_valid_custom_error_response(self, response: Response) -> None:
        """
        Test custom error to make sure the error response has right data format.

        @param response: Response data
        """
        response_data = response.data
        required_fields = ['developer_message', 'user_message', 'error_code']

        for field in required_fields:
            self.assertTrue(field in response_data.keys())

    def tet_pagination(self, response: Response):
        """
        Make sure no missing any data in the pagination response

        @param response: Response data.
        """
        response_json = self.deserialize(response)
        pagination_keys = ['previous', 'next', 'first', 'last', 'self',
                           'count', 'results']

        for key in pagination_keys:
            self.assertTrue(bool(key in response_json.keys()))
