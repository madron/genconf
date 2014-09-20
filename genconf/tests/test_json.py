from django.test import TestCase
from netaddr import IPNetwork
from .. import hardware
from .. import routing
from .. import serializers


class JsonTest(TestCase):
    def test_dump_router(self):
        router = hardware.Router(
            name='Cisco-1801',
            vrfs=[
                routing.Vrf(),
                routing.Vrf(name='voip'),
            ],
            interfaces=[
                hardware.PhysicalInterfaceEthernet(
                    name='Fa0',
                    layer=3,
                    dot1q_mode='trunk',
                    dot1q_encapsulation='802.1q',
                    native_vlan=1,
                    subinterfaces=[
                        routing.SubInterfaceEthernet(
                            name='Fa0.77',
                            layer=3,
                            description='webbrowsing',
                            vlan=77,
                            layer_3_interface=routing.Layer3Interface(
                                ipnetwork=IPNetwork('7.7.7.7/30'),
                            ),
                            notes='Upgrade bandwidth as soon as possible',
                        ),
                        routing.SubInterfaceEthernet(
                            name='Fa0.88',
                            layer=3,
                            description='voip',
                            vlan=88,
                            layer_3_interface=routing.Layer3Interface(
                                ipnetwork=IPNetwork('8.8.8.8/30'),
                                vrf_name='voip',
                            ),
                            notes='Should fallback to webbrowsing interface',
                        ),
                        routing.SubInterfaceEthernet(
                            name='Fa0.1',
                            layer=2,
                            vlan=1,
                        ),
                        routing.SubInterfaceEthernet(
                            name='Fa0.2',
                            layer=2,
                            vlan=2,
                        ),
                    ]
                ),
                hardware.PhysicalInterfaceEthernet(
                    name='Fa1',
                    layer=2,
                    dot1q_mode='access',
                    dot1q_encapsulation='802.1q',
                    native_vlan=10,
                ),
                hardware.PhysicalInterfaceEthernet(
                    name='Fa2',
                    layer=2,
                    dot1q_mode='access',
                    dot1q_encapsulation='802.1q',
                    native_vlan=20,
                ),
                hardware.PhysicalInterfaceEthernet(
                    name='Fa3',
                    layer=2,
                    dot1q_mode='access',
                    dot1q_encapsulation='802.1q',
                    native_vlan=30,
                    description='To voip switch'
                ),
            ],
        )
