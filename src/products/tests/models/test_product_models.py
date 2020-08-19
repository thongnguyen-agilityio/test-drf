from django.test import TestCase

from drf_core.factories import FuzzyText
from products.factories import (
    ProductFactory,
    CategoryFactory,
    SeasonFactory,
    UsageFactory,
    ArticleTypeFactory,
)
from products.models import Product
from .base_test_case import BaseTestCase


class ProductTestCase(BaseTestCase, TestCase):
    Model = Product
    Factory = ProductFactory

    def setUp(self):
        super().setUp()

        # create data
        self.Factory()

    def test_model_can_be_updated(self):

        obj = self.Model.objects.last()

        updated_data = {
            'name': FuzzyText('', 100).fuzz(),
            'category': CategoryFactory(),
            'usage': UsageFactory(),
            'article_type': ArticleTypeFactory(),
            'season': SeasonFactory(),
        }

        for key, value in updated_data.items():
            setattr(obj, key, value)

        obj.save()
        self.assertEqual(obj.category.id, updated_data['category'].id)
        self.assertEqual(obj.usage.id, updated_data['usage'].id)
        self.assertEqual(obj.article_type.id, updated_data['article_type'].id)
        self.assertEqual(obj.season.id, updated_data['season'].id)
        self.assertEqual(obj.name, updated_data['name'])
