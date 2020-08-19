from django.test import TestCase

from products.factories import GenderFactory
from products.models import Gender
from .base_test_case import BaseTestCase


class GenderTestCase(BaseTestCase, TestCase):
    Model = Gender
    Factory = GenderFactory

    def setUp(self):
        super(GenderTestCase, self).setUp()
        self.Factory()
