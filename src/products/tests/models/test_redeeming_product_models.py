from django.test import TestCase
from products.factories import RedeemingProductFactory
from products.models import RedeemingProduct


class RedeemProductTestCase(TestCase):
    Model = RedeemingProduct
    Factory = RedeemingProductFactory

    def setUp(self):
        super().setUp()

        # create data
        self.Factory()

        self.Factory(is_point_kind=True)

    def test_model_can_be_created(self):
        obj1 = self.Model.objects.first()
        self.assertEqual(obj1.id, 1)

        obj2 = self.Model.objects.last()
        self.assertEqual(obj2.id, 2)
