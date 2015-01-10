import netaddr
from django.core import urlresolvers
from django.test import TestCase
from .. import factories
from .. import models


class ProjectModelTest(TestCase):
    def test_str(self):
        project = factories.ProjectFactory(name='Test')
        self.assertEqual(str(project), 'Test')


class RouterModelTest(TestCase):
    def test_str(self):
        router = factories.RouterFactory(name='C1801')
        self.assertEqual(str(router), 'C1801')

    def test_get_url(self):
        router = factories.RouterFactory.create(id=1)
        self.assertEqual(router.get_url(), '/genconf/router/1/')

    def test_get_interface_names_c1801(self):
        router = factories.RouterFactory(model='c1801')
        names = router.get_interface_names()
        self.assertEqual(len(names), 10)
        self.assertEqual(names[0], 'atm0')
        self.assertEqual(names[1], 'fe0')
        self.assertEqual(names[2], 'fe1')
        self.assertEqual(names[9], 'fe8')

    def test_get_interface_names_c1801_atm(self):
        router = factories.RouterFactory(model='c1801')
        names = router.get_interface_names(type='atm')
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], 'atm0')

    def test_get_interface_names_c1801_ethernet(self):
        router = factories.RouterFactory(model='c1801')
        names = router.get_interface_names(type='ethernet')
        self.assertEqual(len(names), 9)
        self.assertEqual(names[0], 'fe0')
        self.assertEqual(names[1], 'fe1')
        self.assertEqual(names[8], 'fe8')

    def test_get_interface_names_c1801_ethernet_layer2(self):
        router = factories.RouterFactory(model='c1801')
        names = router.get_interface_names(type='ethernet', layer=2)
        self.assertEqual(len(names), 8)
        self.assertEqual(names[0], 'fe1')
        self.assertEqual(names[7], 'fe8')

    def test_get_interface_names_c1801_ethernet_layer3(self):
        router = factories.RouterFactory(model='c1801')
        names = router.get_interface_names(type='ethernet', layer=3)
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], 'fe0')

    def test_get_interface_names_c1841(self):
        router = factories.RouterFactory(model='c1841')
        names = router.get_interface_names()
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], 'fe0/0')
        self.assertEqual(names[1], 'fe0/1')

    def test_get_interface_names_c1841_atm(self):
        router = factories.RouterFactory(model='c1841')
        names = router.get_interface_names(type='atm')
        self.assertEqual(len(names), 0)

    def test_get_interface_names_c1841_ethernet(self):
        router = factories.RouterFactory(model='c1841')
        names = router.get_interface_names(type='ethernet')
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], 'fe0/0')
        self.assertEqual(names[1], 'fe0/1')

    def test_get_interface_names_c1841_ethernet_layer2(self):
        router = factories.RouterFactory(model='c1841')
        names = router.get_interface_names(type='ethernet', layer=2)
        self.assertEqual(len(names), 0)

    def test_get_interface_names_c1841_ethernet_layer3(self):
        router = factories.RouterFactory(model='c1841')
        names = router.get_interface_names(type='ethernet', layer=3)
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], 'fe0/0')
        self.assertEqual(names[1], 'fe0/1')


class VrfModelTest(TestCase):
    def test_str(self):
        vrf = factories.VrfFactory(name='')
        self.assertEqual(str(vrf), '(default)')

    def test_delete_vrf_link(self):
        vrf = factories.VrfFactory(id=1, name='vrf')
        self.assertEqual(vrf.delete_vrf_link(), '<a href="/genconf/vrf/1/delete/">vrf</a>')

    def test_delete_vrf_link_default(self):
        vrf = factories.VrfFactory(name='')
        self.assertEqual(vrf.delete_vrf_link(), '(default)')

    def test_delete_vrf_link_not_saved(self):
        vrf = models.Vrf(name='vrf')
        self.assertEqual(vrf.delete_vrf_link(), '')


class RouteModelTest(TestCase):
    def test_str(self):
        route = factories.RouteFactory(name='test')
        self.assertEqual(str(route), 'test')


class Layer3InterfaceModelTest(TestCase):
    def test_str(self):
        interface = factories.Layer3InterfaceFactory(
            ipnetwork=netaddr.IPNetwork('192.168.1.1/24'))
        self.assertEqual(str(interface), '192.168.1.1/24')


class VlanModelTest(TestCase):
    def test_str_tag(self):
        vlan = factories.VlanFactory(tag=2)
        self.assertEqual(str(vlan), '2')

    def test_str_description(self):
        vlan = factories.VlanFactory(tag=2, description='Wan')
        self.assertEqual(str(vlan), '2 (Wan)')


class PhysicalInterfaceModelTest(TestCase):
    def test_str_no_router_name(self):
        interface = factories.PhysicalInterfaceFactory(name='Fa0')
        self.assertEqual(str(interface), 'Fa0')

    def test_str(self):
        interface = factories.PhysicalInterfaceFactory(router__name='Main', name='Fa0')
        self.assertEqual(str(interface), 'Main Fa0')

    def test_layer2(self):
        interface = factories.PhysicalInterfaceFactory(layer=2)
        self.assertTrue(interface.is_layer2)
        self.assertFalse(interface.is_layer3)

    def test_layer3(self):
        interface = factories.PhysicalInterfaceFactory(layer=3)
        self.assertFalse(interface.is_layer2)
        self.assertTrue(interface.is_layer3)

    def test_get_url(self):
        router = factories.PhysicalInterfaceFactory.create(id=1)
        self.assertEqual(router.get_url(), '/genconf/physicalinterface/1/')


class SubInterfaceModelTest(TestCase):
    def test_str(self):
        interface = factories.SubInterfaceFactory(name='Fa1.4')
        self.assertEqual(str(interface), 'Fa1.4')

    def test_get_url(self):
        interface = factories.SubInterfaceFactory.create(id=1)
        self.assertEqual(interface.get_url(), '/genconf/subinterface/1/')
