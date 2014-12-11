from unittest import skip
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import UserFactory
from .. import factories
from .. import models


class ProjectAdminWizardTest(TestCase):
    def setUp(self):
        UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:genconf_projectwizard_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:genconf_projectwizard_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        obj = factories.ProjectFactory(name='Project name')
        url = reverse('admin:genconf_projectwizard_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'value="Project name"')

    def test_delete(self):
        obj = factories.ProjectFactory()
        url = reverse('admin:genconf_projectwizard_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


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

    def test_delete(self):
        obj = factories.RouterFactory()
        url = reverse('admin:genconf_router_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_configuration(self):
        obj = factories.RouterFactory()
        url = reverse('admin:genconf_router_configuration', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'no aaa new-model')


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
