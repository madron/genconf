from django.test import TestCase
from . import factories
from .. import models


class ProjectModelTest(TestCase):
    def test_str(self):
        project = factories.ProjectFactory(name='Test')
        self.assertEqual(str(project), 'Test')


class RouterModelTest(TestCase):
    def test_str(self):
        router = factories.RouterFactory(name='C1801')
        self.assertEqual(str(router), 'C1801')


class VrfModelTest(TestCase):
    def test_str(self):
        vrf = factories.VrfFactory(name='')
        self.assertEqual(str(vrf), '<default>')


class RouteModelTest(TestCase):
    def test_str(self):
        route = factories.RouteFactory(name='test')
        self.assertEqual(str(route), 'test')


class Layer3InterfaceModelTest(TestCase):
    def test_str(self):
        interface = factories.Layer3InterfaceFactory(description='test')
        self.assertEqual(str(interface), 'test')


class VlanModelTest(TestCase):
    def test_str_tag(self):
        vlan = factories.VlanFactory(tag=2)
        self.assertEqual(str(vlan), '2')

    def test_str_description(self):
        vlan = factories.VlanFactory(tag=2, description='Wan')
        self.assertEqual(str(vlan), '2 (Wan)')


class PhysicalInterfaceModelTest(TestCase):
    def test_str(self):
        interface = factories.PhysicalInterfaceFactory(name='Fa0')
        self.assertEqual(str(interface), 'Fa0')

    def test_layer2(self):
        interface = factories.PhysicalInterfaceFactory(layer=2)
        self.assertTrue(interface.is_layer2)
        self.assertFalse(interface.is_layer3)

    def test_layer3(self):
        interface = factories.PhysicalInterfaceFactory(layer=3)
        self.assertFalse(interface.is_layer2)
        self.assertTrue(interface.is_layer3)


class SubInterfaceModelTest(TestCase):
    def test_str(self):
        interface = factories.SubInterfaceFactory(name='Fa1.4')
        self.assertEqual(str(interface), 'Fa1.4')
