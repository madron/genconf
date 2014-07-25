from django.test import TestCase
from netaddr import IPNetwork
from .. import config


class LanConfigTest(TestCase):
    def test_init(self):
        lan = dict(
            subnet='192.168.20.45/24',
        )
        lan = config.LanConfig(lan)
        self.assertEqual(lan['subnet'], IPNetwork('192.168.20.45/24'))

    def test_set(self):
        lan = config.LanConfig()
        lan['subnet'] = '192.168.20.45/24'
        self.assertEqual(lan['subnet'], IPNetwork('192.168.20.45/24'))
