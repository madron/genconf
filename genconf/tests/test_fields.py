from django.core.exceptions import ValidationError
from django.test import TestCase
from netaddr import IPAddress
from .. import fields


class IPAddressFieldTest(TestCase):
    def test_empty(self):
        f = fields.IPAddressField(required=False)
        self.assertEqual(f.clean(''), None)
        self.assertEqual(f.clean(' '), None)

    def test_ipv4_ok(self):
        f = fields.IPAddressField()
        self.assertEqual(f.clean('8.8.8.8'), IPAddress('8.8.8.8'))
        self.assertEqual(f.clean('151.1.1.1'), IPAddress('151.1.1.1'))
        self.assertEqual(f.clean('172.16.1.1'), IPAddress('172.16.1.1'))
        self.assertEqual(f.clean('192.168.1.1'), IPAddress('192.168.1.1'))
        self.assertEqual(f.clean(' 192.168.1.1'), IPAddress('192.168.1.1'))
        self.assertEqual(f.clean(' 192.168.1.1 '), IPAddress('192.168.1.1'))

    def test_ipv4_ko(self):
        f = fields.IPAddressField()
        self.assertRaises(ValidationError, f.clean, '192.168.1.1.1')
        self.assertRaises(ValidationError, f.clean, '192.168.1.300')

    def test_ipv6_ok(self):
        f = fields.IPAddressField()
        self.assertEqual(f.clean('fe80::'), IPAddress('fe80::'))

    def test_ipv6_ko(self):
        f = fields.IPAddressField()
        self.assertRaises(ValidationError, f.clean, 'ge80::')
