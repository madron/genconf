from django.test import TestCase
from netaddr import IPNetwork
from .. import hardware
from .. import routing
from .. import serializers


class JsonTest(TestCase):
    def test_dump_router(self):
        router = hardware.Router(
            name='Cisco-1801',
            interfaces=[
                hardware.PhysicalInterfaceEthernet(
                    name='Fa0',
                    layer=3,
                    dot1q_mode='trunk',
                    dot1q_encapsulation='802.1q',
                    native_vlan=1,
                    subinterfaces=[
                        routing.SubInterfaceEthernet(
                            name='Fa0.99',
                            layer=3,
                            description='wan1',
                            vlan=99,
                            layer_3_interface=routing.Layer3Interface(
                                ipnetwork=IPNetwork('7.7.7.7/30')
                            )
                        ),
                        routing.SubInterfaceEthernet(
                            name='Fa0.1',
                            layer=2,
                            vlan=1,
                            description='lan1',
                        ),
                        routing.SubInterfaceEthernet(
                            name='Fa0.2',
                            layer=2,
                            vlan=2,
                            description='lan2',
                        ),
                    ]
                ),
                hardware.PhysicalInterfaceEthernet(
                    name='Fa1',
                    layer=2,
                    dot1q_mode='access',
                    dot1q_encapsulation='802.1q',
                    native_vlan=1,
                ),
                hardware.PhysicalInterfaceEthernet(
                    name='Fa2',
                    layer=2,
                    dot1q_mode='access',
                    dot1q_encapsulation='802.1q',
                    native_vlan=2,
                ),
            ],
        )
