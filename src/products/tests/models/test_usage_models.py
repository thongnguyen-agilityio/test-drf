from django.test import TestCase
from products.factories import UsageFactory
from products.models import Usage


class UsageTestCase(TestCase):
    Model = Usage
    Factory = UsageFactory

    def setUp(self):
        super().setUp()

        # create data
        self.Factory()
