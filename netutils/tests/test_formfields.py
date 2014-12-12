from django.core.exceptions import ValidationError
from django.test import TestCase
from netaddr import IPAddress, IPNetwork
from .. import formfields


class IPAddressFieldTest(TestCase):
    def test_protocol(self):
        formfields.NetIPAddressField()
        formfields.NetIPAddressField(protocol='both')
        formfields.NetIPAddressField(protocol='ipv4')
        formfields.NetIPAddressField(protocol='ipv6')
        self.assertRaises(ValueError, formfields.NetIPAddressField, protocol='wrong')

    def test_empty(self):
        f = formfields.NetIPAddressField(required=False)
        self.assertEqual(f.clean(''), None)
        self.assertEqual(f.clean(' '), None)

    def test_ipv4_ok(self):
        f = formfields.NetIPAddressField()
        self.assertEqual(f.clean('8.8.8.8'), IPAddress('8.8.8.8'))
        self.assertEqual(f.clean('151.1.1.1'), IPAddress('151.1.1.1'))
        self.assertEqual(f.clean('172.16.1.1'), IPAddress('172.16.1.1'))
        self.assertEqual(f.clean('192.168.1.1'), IPAddress('192.168.1.1'))
        self.assertEqual(f.clean(' 192.168.1.1'), IPAddress('192.168.1.1'))
        self.assertEqual(f.clean(' 192.168.1.1 '), IPAddress('192.168.1.1'))

    def test_ipv4_ko(self):
        f = formfields.NetIPAddressField()
        self.assertRaises(ValidationError, f.clean, '192.168.1.1.1')
        self.assertRaises(ValidationError, f.clean, '192.168.1.300')

    def test_ipv4_only(self):
        f = formfields.NetIPAddressField(protocol='ipv4')
        self.assertEqual(f.clean('127.0.0.1'), IPAddress('127.0.0.1'))
        self.assertRaises(ValidationError, f.clean, 'fe80::')

    def test_ipv6_ok(self):
        f = formfields.NetIPAddressField()
        self.assertEqual(f.clean('fe80::'), IPAddress('fe80::'))

    def test_ipv6_ko(self):
        f = formfields.NetIPAddressField()
        self.assertRaises(ValidationError, f.clean, 'ge80::')

    def test_ipv6_only(self):
        f = formfields.NetIPAddressField(protocol='ipv6')
        self.assertEqual(f.clean('fe80::'), IPAddress('fe80::'))
        self.assertRaises(ValidationError, f.clean, '127.0.0.1')


class IPNetworkFieldTest(TestCase):
    def test_protocol(self):
        formfields.NetIPNetworkField()
        formfields.NetIPNetworkField(protocol='both')
        formfields.NetIPNetworkField(protocol='ipv4')
        formfields.NetIPNetworkField(protocol='ipv6')
        self.assertRaises(ValueError, formfields.NetIPNetworkField, protocol='wrong')

    def test_empty(self):
        f = formfields.NetIPNetworkField(required=False)
        self.assertEqual(f.clean(''), None)
        self.assertEqual(f.clean(' '), None)

    def test_ipv4_ok(self):
        f = formfields.NetIPNetworkField()
        self.assertEqual(f.clean('8.8.8.8'), IPNetwork('8.8.8.8/32'))
        self.assertEqual(f.clean('8.8.8.8/32'), IPNetwork('8.8.8.8/32'))
        self.assertEqual(f.clean('151.1.1.1/16'), IPNetwork('151.1.1.1/16'))
        self.assertEqual(f.clean('172.16.1.1/16'), IPNetwork('172.16.1.1/16'))
        self.assertEqual(f.clean('192.168.1.1/24'), IPNetwork('192.168.1.1/24'))
        self.assertEqual(f.clean(' 192.168.1.1/24'), IPNetwork('192.168.1.1/24'))
        self.assertEqual(f.clean(' 192.168.1.1/30 '), IPNetwork('192.168.1.1/30'))

    def test_ipv4_ko(self):
        f = formfields.NetIPNetworkField()
        self.assertRaises(ValidationError, f.clean, '192.168.1.1/33')
        self.assertRaises(ValidationError, f.clean, '192.168.1.300/24')

    def test_ipv4_only(self):
        f = formfields.NetIPNetworkField(protocol='ipv4')
        self.assertEqual(f.clean('127.0.0.1/32'), IPNetwork('127.0.0.1/32'))
        self.assertRaises(ValidationError, f.clean, 'fe80::/48')

    def test_ipv6_ok(self):
        f = formfields.NetIPNetworkField()
        self.assertEqual(f.clean('fe80::/64'), IPNetwork('fe80::/64'))

    def test_ipv6_ko(self):
        f = formfields.NetIPNetworkField()
        self.assertRaises(ValidationError, f.clean, 'ge80::/24')

    def test_ipv6_only(self):
        f = formfields.NetIPNetworkField(protocol='ipv6')
        self.assertEqual(f.clean('fe80::/128'), IPNetwork('fe80::/128'))
        self.assertRaises(ValidationError, f.clean, '127.0.0.1/32')
