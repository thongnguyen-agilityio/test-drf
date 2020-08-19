from django.test import TestCase

from products.factories import ArticleTypeFactory
from products.models import ArticleType


class ArticleTypeTestCase(TestCase):
    Model = ArticleType
    Factory = ArticleTypeFactory

    def setUp(self):
        super().setUp()

        # create data
        self.Factory()
