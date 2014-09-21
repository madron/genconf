from django.test import TestCase
from netaddr import IPNetwork
from .. import routing


class RouteTest(TestCase):
    def test_init(self):
        route = routing.Route()
        self.assertEqual(route.name, '')
        self.assertEqual(route.network, None)
        self.assertEqual(route.next_hop, None)
        self.assertEqual(route.metric, 1)
        self.assertEqual(route.tag, None)


class VrfTest(TestCase):
    def test_init(self):
        vrf = routing.Vrf()
        self.assertEqual(vrf.name, '')
        self.assertEqual(vrf.default_gateway, None)
        self.assertEqual(vrf.static_routes, [])

    def test_global(self):
        self.assertTrue(routing.Vrf().is_global)
        self.assertFalse(routing.Vrf(name='other').is_global)


class Layer2InterfaceTest(TestCase):
    def test_init(self):
        l2 = routing.Layer2Interface()
        self.assertEqual(l2.description, '')
        self.assertEqual(l2.mode, 'access')
        self.assertEqual(l2.vlan, 1)
        self.assertEqual(l2.allowed_vlans, 'all')
        self.assertEqual(l2.encapsulation, '802.1q')
        self.assertEqual(l2.stp_bpdu_filter, True)
        self.assertEqual(l2.stp_portfast, True)
        self.assertEqual(l2.broadcast_level_percentage, 5)


class Layer3InterfaceTest(TestCase):
    def test_init(self):
        l3 = routing.Layer3Interface()
        self.assertEqual(l3.description, '')
        self.assertEqual(l3.ipnetwork, None)
        self.assertEqual(l3.vrf_name, '')

    def test_equal(self):
        self.assertEqual(routing.Layer3Interface(), routing.Layer3Interface())
        if1 = routing.Layer3Interface(ipnetwork='192.168.1.1/24')
        if2 = routing.Layer3Interface(ipnetwork=IPNetwork('192.168.1.1/24'))
        self.assertEqual(if1, if2)


class VlanTest(TestCase):
    def test_init_default(self):
        vlan = routing.Vlan()
        self.assertEqual(vlan.tag, 1)
        self.assertEqual(vlan.layer_3_interface, None)
        self.assertEqual(vlan.description, '')
        self.assertEqual(vlan.notes, '')


class SubInterfaceTest(TestCase):
    def test_init_default(self):
        subif = routing.SubInterface()
        self.assertEqual(subif.name, '')
        self.assertEqual(subif.layer_3_interface, None)
        self.assertEqual(subif.description, '')
        self.assertEqual(subif.notes, '')


class SubInterfaceEthernetTest(TestCase):
    def test_init_default(self):
        subif = routing.SubInterfaceEthernet()
        self.assertEqual(subif.name, '')
        self.assertEqual(subif.layer_3_interface, None)
        self.assertEqual(subif.description, '')
        self.assertEqual(subif.notes, '')
        self.assertEqual(subif.layer, 3)
        self.assertEqual(subif.vlan, 1)


class SubInterfaceAtmTest(TestCase):
    def test_init_default(self):
        subif = routing.SubInterfaceAtm()
        self.assertEqual(subif.name, '')
        self.assertEqual(subif.layer_3_interface, None)
        self.assertEqual(subif.description, '')
        self.assertEqual(subif.notes, '')
        self.assertEqual(subif.link, 'point-to-point')
        self.assertEqual(subif.pvc_vp, '8')
        self.assertEqual(subif.pvc_vc, '35')
        self.assertEqual(subif.pvc_encapsulation, 'pppoa')
        self.assertEqual(subif.pvc_mux, 'vc-mux')
        self.assertEqual(subif.pvc_dialer_pool_number, 1)
