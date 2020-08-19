from django.test import TestCase

from products.factories import BaseColourFactory
from products.models import BaseColour
from .base_test_case import BaseTestCase


class BaseColourTestCase(BaseTestCase, TestCase):
    Model = BaseColour
    Factory = BaseColourFactory

    def setUp(self):
        super().setUp()

        # create data
        self.Factory()
