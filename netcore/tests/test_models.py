from django.test import TestCase
from . import factories


class BrasModelTest(TestCase):
    def test_str(self):
        bras = factories.BrasFactory(name='Test')
        self.assertEqual(str(bras), 'Test')
