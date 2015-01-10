import netaddr
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import UserFactory
from .. import factories


class ProjectAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_project_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_project_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.ProjectFactory(name='Project name')
        url = reverse('admin:genconf_project_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'value="Project name"')

    def test_delete(self):
        obj = factories.ProjectFactory()
        url = reverse('admin:genconf_project_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProjectCustomAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_projectcustom_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_projectcustom_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.ProjectFactory(name='Project name')
        url = reverse('admin:genconf_projectcustom_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'value="Project name"')

    def test_detail_physical_link(self):
        project_1 = factories.ProjectFactory(name='Project 1')
        project_2 = factories.ProjectFactory(name='Project 2')
        router_1 = factories.RouterFactory(project=project_1, name='R1')
        router_2 = factories.RouterFactory(project=project_2, name='R2')
        factories.PhysicalInterfaceFactory(name='Fa1Interface', router=router_1)
        factories.PhysicalInterfaceFactory(name='Fa2Interface', router=router_2)
        url = reverse('admin:genconf_projectcustom_change', args=(project_1.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'Fa1Interface')
        self.assertNotContains(response, 'Fa2Interface')

    def test_delete(self):
        obj = factories.ProjectFactory()
        url = reverse('admin:genconf_projectcustom_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProjectCpe2AdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_projectcpe2_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_project_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.ProjectFactory(name='Project name', wizard='cpe2')
        url = reverse('admin:genconf_projectcpe2_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'value="Project name"')

    def test_detail_not_found(self):
        obj = factories.ProjectFactory(name='Project name')
        url = reverse('admin:genconf_projectcpe2_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        obj = factories.ProjectFactory(wizard='cpe2')
        url = reverse('admin:genconf_projectcpe2_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_not_found(self):
        obj = factories.ProjectFactory()
        url = reverse('admin:genconf_projectcpe2_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RouterAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_router_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_router_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.RouterFactory()
        interface = factories.PhysicalInterfaceFactory(router=obj)
        url = reverse('admin:genconf_router_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response,
            reverse('admin:genconf_router_configuration', args=(obj.pk,)))
        self.assertContains(response,
            reverse('admin:genconf_physicalinterface_change', args=(interface.pk,)))

    def test_detail_wizard(self):
        obj = factories.RouterFactory(project__wizard='cpe2')
        url = reverse('admin:genconf_router_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_native_vlan(self):
        router_1 = factories.RouterFactory(id=1, name='r1')
        router_2 = factories.RouterFactory(id=2, name='r2')
        factories.VlanFactory(router=router_1, tag=1, description='VLAN_1')
        factories.VlanFactory(router=router_2, tag=2, description='VLAN_2')
        factories.PhysicalInterfaceFactory(router=router_1)
        url = reverse('admin:genconf_router_change', args=(router_1.pk,))
        response = self.client.get(url)
        self.assertContains(response, '1 (VLAN_1)')
        self.assertNotContains(response, '2 (VLAN_2)')

    def test_detail_vlan_vrf(self):
        router_1 = factories.RouterFactory(id=1, name='r1')
        router_2 = factories.RouterFactory(id=2, name='r2')
        factories.VrfFactory(router=router_1, name='VRF_1')
        factories.VrfFactory(router=router_2, name='VRF_2')
        vlan = factories.VlanFactory(router=router_1, tag=2)
        url = reverse('admin:genconf_router_change', args=(router_1.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'VRF_1')
        self.assertNotContains(response, 'VRF_2')

    def test_delete(self):
        obj = factories.RouterFactory()
        url = reverse('admin:genconf_router_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_wizard(self):
        obj = factories.RouterFactory(project__wizard='cpe2')
        url = reverse('admin:genconf_router_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_configuration(self):
        router = factories.RouterFactory(name='wan1')
        vrf = factories.VrfFactory(router=router)
        factories.VrfFactory(router=router, name='voip')
        vlan_1 = factories.VlanFactory(router=router, tag=1)
        vlan_2 = factories.VlanFactory(router=router, tag=2, description='Voip')
        fe0 = factories.PhysicalInterfaceFactory(router=router, name='fe0', layer=3)
        fe1 = factories.PhysicalInterfaceFactory(router=router, name='fe1', layer=2)
        l3 = factories.Layer3InterfaceFactory(vrf=vrf, ipnetwork=netaddr.IPNetwork('172.18.1.1/16'))
        factories.SubInterfaceFactory(physical_interface=fe0, name='fe0.1', vlan=vlan_1, layer_3_interface=l3)
        l3 = factories.Layer3InterfaceFactory(vrf=vrf, ipnetwork=netaddr.IPNetwork('192.168.5.1/24'))
        factories.SubInterfaceFactory(physical_interface=fe0, name='fe0.2', vlan=vlan_2, layer_3_interface=l3)
        factories.SubInterfaceFactory(physical_interface=fe1, name='fe1.2', vlan=vlan_2)
        url = reverse('admin:genconf_router_configuration', args=(router.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'no aaa new-model')
        # Vrf
        self.assertContains(response, 'ip vrf voip')
        # Vlan
        self.assertContains(response, 'vlan 2')
        self.assertContains(response, '    name Voip')
        # Interfaces
        self.assertContains(response, 'interface fe0.2')
        self.assertContains(response, 'vrf voip')
        self.assertContains(response, 'ip address 192.168.5.1 255.255.255.0')


class VrfAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_vrf_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 403)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 403)

    def test_add(self):
        url = reverse('admin:genconf_vrf_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.VrfFactory()
        url = reverse('admin:genconf_vrf_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        obj = factories.VrfFactory(name='notdefault')
        url = reverse('admin:genconf_vrf_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_default(self):
        obj = factories.VrfFactory()
        url = reverse('admin:genconf_vrf_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class RouteAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_route_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_route_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.RouteFactory()
        url = reverse('admin:genconf_route_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.RouteFactory()
        url = reverse('admin:genconf_route_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class VlanAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_vlan_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_vlan_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.VlanFactory()
        url = reverse('admin:genconf_vlan_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.VlanFactory()
        url = reverse('admin:genconf_vlan_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class PhysicalInterfaceAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_physicalinterface_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_physicalinterface_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        project = factories.ProjectFactory(name='name')
        obj = factories.PhysicalInterfaceFactory(router__project=project)
        subif = factories.SubInterfaceFactory(physical_interface=obj)
        url = reverse('admin:genconf_physicalinterface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            reverse('admin:genconf_subinterface_change', args=(subif.pk,)))

    def test_detail_not_found(self):
        project = factories.ProjectFactory(name='name', wizard='cpe2')
        router = factories.RouterFactory(project=project)
        obj = factories.PhysicalInterfaceFactory(router=router)
        url = reverse('admin:genconf_physicalinterface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_subinterface_vrf(self):
        router_1 = factories.RouterFactory(id=1, name='r1')
        router_2 = factories.RouterFactory(id=2, name='r2')
        factories.VrfFactory(router=router_1, name='VRF_1')
        factories.VrfFactory(router=router_2, name='VRF_2')
        pif = factories.PhysicalInterfaceFactory(router=router_1)
        factories.SubInterfaceFactory(physical_interface=pif)
        url = reverse('admin:genconf_physicalinterface_change', args=(router_1.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'VRF_1')
        self.assertNotContains(response, 'VRF_2')

    def test_delete(self):
        obj = factories.PhysicalInterfaceFactory()
        url = reverse('admin:genconf_physicalinterface_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SubInterfaceAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_subinterface_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_subinterface_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        obj = factories.SubInterfaceFactory()
        url = reverse('admin:genconf_subinterface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_found(self):
        project = factories.ProjectFactory(name='name', wizard='cpe2')
        router = factories.RouterFactory(project=project)
        pif = factories.PhysicalInterfaceFactory(router=router)
        obj = factories.SubInterfaceFactory(physical_interface=pif)
        url = reverse('admin:genconf_subinterface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        obj = factories.SubInterfaceFactory()
        url = reverse('admin:genconf_subinterface_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PhysicalLinkAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_physicallink_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_physicallink_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.PhysicalLinkFactory()
        url = reverse('admin:genconf_physicallink_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.PhysicalLinkFactory()
        url = reverse('admin:genconf_physicallink_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class Layer3InterfaceAdminTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_layer3interface_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_layer3interface_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.Layer3InterfaceFactory()
        url = reverse('admin:genconf_layer3interface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.Layer3InterfaceFactory()
        url = reverse('admin:genconf_layer3interface_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
