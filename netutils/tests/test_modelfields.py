from django.test import TestCase
from netaddr import IPAddress
from .. import formfields
from .. import modelfields


class NetIPAddressFieldTest(TestCase):
    def test_to_python(self):
        f = modelfields.NetIPAddressField()
        self.assertEqual(f.to_python(None), None)
        self.assertEqual(f.to_python('0.0.0.0'), IPAddress('0.0.0.0'))
        self.assertEqual(f.to_python('127.0.0.1'), IPAddress('127.0.0.1'))

    def test_get_prep_value(self):
        f = modelfields.NetIPAddressField()
        self.assertEqual(f.get_prep_value(''), None)
        self.assertEqual(f.get_prep_value(None), None)
        self.assertEqual(f.get_prep_value(IPAddress('127.0.0.1')), '127.0.0.1')

    def test_formfield(self):
        f = modelfields.NetIPAddressField().formfield()
        self.assertIsInstance(f, formfields.IPAddressField)
        self.assertEqual(f.clean('127.0.0.1'), IPAddress('127.0.0.1'))
