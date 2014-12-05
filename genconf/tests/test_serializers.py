import json
import netaddr
from django.test import TestCase
from .. import serializers


class ProjectEncoderTest(TestCase):
    def test_dump(self):
        data = dict(
            router='c1841',
            ip=netaddr.IPAddress('151.1.1.1'),
            network=netaddr.IPNetwork('8.8.8.8/16'),
        )
        json_data = json.dumps(data, cls=serializers.ProjectEncoder)
        self.assertTrue('"ip": "151.1.1.1"' in json_data)
        self.assertTrue('"network": "8.8.8.8/16"' in json_data)
