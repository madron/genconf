from django.test import TestCase
from . import factories


class BrasModelTest(TestCase):
    def test_str(self):
        bras = factories.BrasFactory(name='Test')
        self.assertEqual(str(bras), 'Test')


class VrfModelTest(TestCase):
    def test_str(self):
        vrf = factories.VrfFactory(number=1, name='first', bras__name='brasname')
        self.assertEqual(str(vrf), '1 first (brasname)')
