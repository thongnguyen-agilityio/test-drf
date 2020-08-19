from drf_core.factories import FuzzyText


class BaseTestCase:
    Model = None
    Factory = None

    def setUp(self):
        pass

    def tearDown(self):
        self.Model.objects.all().delete()

    def test_model_can_be_created(self):
        obj = self.Model.objects.first()
        self.assertEqual(obj.id, 1)

    def test_model_can_be_updated(self):
        data = {
            'name': FuzzyText('', 100).fuzz()
        }

        # Create new one
        obj = self.Factory()

        # Update
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()

        # Check data
        self.assertEqual(obj.name, data['name'])

    def test_model_can_be_deleted(self):
        obj = self.Factory()
        obj.delete()

        # Check deleted data
        self.assertEqual(obj.id, None)
