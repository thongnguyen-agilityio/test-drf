from django.test import TestCase
from products.factories import SeasonFactory
from products.models import Season
from .base_test_case import BaseTestCase


class SeasonTestCase(BaseTestCase, TestCase):
    Model = Season
    Factory = SeasonFactory

    def setUp(self):
        super().setUp()
        self.Factory()
