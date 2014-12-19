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
        url = reverse('admin:genconf_router_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response,
            reverse('admin:genconf_router_configuration', args=(obj.pk,)))

    def test_detail_wizard(self):
        obj = factories.RouterFactory(project__wizard='cpe2')
        url = reverse('admin:genconf_router_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

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
        vrf_voip = factories.VrfFactory(router=router, name='voip')
        vlan_1 = factories.VlanFactory(router=router, tag=1)
        vlan_2 = factories.VlanFactory(router=router, tag=2, description='Voip')
        fe0 = factories.PhysicalInterfaceFactory(router=router, name='fe0', layer=3)
        fe1 = factories.PhysicalInterfaceFactory(router=router, name='fe1', layer=2)
        subif = factories.SubInterfaceFactory(physical_interface=fe0, name='fe0.1', vlan=vlan_1)
        factories.Layer3InterfaceFactory(subinterface=subif, vrf=vrf, ipnetwork=netaddr.IPNetwork('172.18.1.1/16'))
        subif = factories.SubInterfaceFactory(physical_interface=fe0, name='fe0.2', vlan=vlan_2)
        factories.Layer3InterfaceFactory(subinterface=subif, vrf=vrf_voip, ipnetwork=netaddr.IPNetwork('192.168.5.1/24'))
        subif = factories.SubInterfaceFactory(physical_interface=fe1, name='fe1.2', vlan=vlan_2)
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
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_vrf_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.VrfFactory()
        url = reverse('admin:genconf_vrf_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
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
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.PhysicalInterfaceFactory()
        url = reverse('admin:genconf_physicalinterface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.PhysicalInterfaceFactory()
        url = reverse('admin:genconf_physicalinterface_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


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
        self.assertEqual(response.status_code, 403)

    def test_detail(self):
        obj = factories.SubInterfaceFactory()
        url = reverse('admin:genconf_subinterface_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.SubInterfaceFactory()
        url = reverse('admin:genconf_subinterface_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


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
