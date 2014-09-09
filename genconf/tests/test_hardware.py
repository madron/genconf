from django.test import TestCase
from netaddr import IPNetwork
from .. import hardware


class PhysicalInterfaceTest(TestCase):
    def test_init(self):
        pif = hardware.PhysicalInterface(name='Fa0/1', type='atm', layers=[3])
        self.assertEqual(pif.name, 'Fa0/1')
        self.assertEqual(pif.type, 'atm')
        self.assertEqual(pif.layers, [3])

    def test_init_empty(self):
        pif = hardware.PhysicalInterface()
        self.assertEqual(pif.name, '')
        self.assertEqual(pif.type, 'ethernet')
        self.assertEqual(pif.layers, [])

    def test_is_layer(self):
        pif = hardware.PhysicalInterface()
        self.assertFalse(pif.is_layer2)
        self.assertFalse(pif.is_layer3)
        pif = hardware.PhysicalInterface(layers=[2])
        self.assertTrue(pif.is_layer2)
        self.assertFalse(pif.is_layer3)
        pif = hardware.PhysicalInterface(layers=[3])
        self.assertFalse(pif.is_layer2)
        self.assertTrue(pif.is_layer3)
        pif = hardware.PhysicalInterface(layers=(2, 3))
        self.assertTrue(pif.is_layer2)
        self.assertTrue(pif.is_layer3)
        # Change layers
        pif.layers = [2]
        self.assertTrue(pif.is_layer2)
        self.assertFalse(pif.is_layer3)


class PhysicalInterfaceEthernetTest(TestCase):
    def test_init(self):
        pif = hardware.PhysicalInterfaceEthernet(
            name='FastEthernet0/1',
            type='will be overwritten',
            layers=[2, 3],
            mtu=1460,
            dot1q_mode='trunk',
            native_vlan=9
        )
        self.assertEqual(pif.name, 'FastEthernet0/1')
        self.assertEqual(pif.type, 'ethernet')
        self.assertEqual(pif.layers, [2, 3])
        self.assertEqual(pif.mtu, 1460)
        self.assertEqual(pif.speed, 'auto')
        self.assertEqual(pif.dot1q_mode, 'trunk')
        self.assertEqual(pif.native_vlan, 9)

    def test_init_empty(self):
        pif = hardware.PhysicalInterfaceEthernet()
        self.assertEqual(pif.name, '')
        self.assertEqual(pif.type, 'ethernet')
        self.assertEqual(pif.layers, [])
        self.assertEqual(pif.mtu, 1500)
        self.assertEqual(pif.speed, 'auto')
