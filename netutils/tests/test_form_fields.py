from django.core.exceptions import ValidationError
from django.test import TestCase
from netaddr import IPAddress, IPNetwork
from .. import form_fields as fields


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


class IPNetworkFieldTest(TestCase):
    def test_empty(self):
        f = fields.IPNetworkField(required=False)
        self.assertEqual(f.clean(''), None)
        self.assertEqual(f.clean(' '), None)

    def test_ipv4_ok(self):
        f = fields.IPNetworkField()
        self.assertEqual(f.clean('8.8.8.8'), IPNetwork('8.8.8.8/32'))
        self.assertEqual(f.clean('8.8.8.8/32'), IPNetwork('8.8.8.8/32'))
        self.assertEqual(f.clean('151.1.1.1/16'), IPNetwork('151.1.1.1/16'))
        self.assertEqual(f.clean('172.16.1.1/16'), IPNetwork('172.16.1.1/16'))
        self.assertEqual(f.clean('192.168.1.1/24'), IPNetwork('192.168.1.1/24'))
        self.assertEqual(f.clean(' 192.168.1.1/24'), IPNetwork('192.168.1.1/24'))
        self.assertEqual(f.clean(' 192.168.1.1/30 '), IPNetwork('192.168.1.1/30'))

    def test_ipv4_ko(self):
        f = fields.IPNetworkField()
        self.assertRaises(ValidationError, f.clean, '192.168.1.1/33')
        self.assertRaises(ValidationError, f.clean, '192.168.1.300/24')
