from django.test import TestCase

from drf_core.factories import FuzzyText
from products.factories import CategoryFactory
from products.models import Category
from .base_test_case import BaseTestCase


class CategoryTestCase(BaseTestCase, TestCase):
    Model = Category
    Factory = CategoryFactory

    def setUp(self):
        super().setUp()

        # create data
        self.Factory()

    def test_model_can_be_updated(self):
        update_data = {
            'parent': self.Factory(),
            'name': FuzzyText('', 100).fuzz(),
        }

        obj = self.Model.objects.last()
        for key, value in update_data.items():
            setattr(obj, key, value)

        obj.save()

        self.assertTrue(isinstance(obj.parent, self.Model))
        self.assertEqual(obj.name, update_data['name'])
