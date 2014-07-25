from django.test import TestCase
from netaddr import IPNetwork
from .. import config


class LanConfigTest(TestCase):
    def test_init_empty(self):
        lan = config.LanConfig()
        self.assertEqual(lan.description, '')
        self.assertEqual(lan.subnet, None)

    def test_init(self):
        lan = config.LanConfig(description='Test Lan', subnet='192.168.20.45/24')
        self.assertEqual(lan.description, 'Test Lan')
        self.assertEqual(lan.subnet, IPNetwork('192.168.20.45/24'))

    def test_subnet_set(self):
        lan = config.LanConfig()
        lan.subnet = '192.168.20.45/24'
        self.assertEqual(lan.subnet, IPNetwork('192.168.20.45/24'))
        lan.subnet = IPNetwork('192.168.20.45/24')
        self.assertEqual(lan.subnet, IPNetwork('192.168.20.45/24'))

    def test_subnet_set_null(self):
        lan = config.LanConfig()
        lan.subnet = None
        self.assertEqual(lan.subnet, None)
        lan.subnet = ''
        self.assertEqual(lan.subnet, None)
