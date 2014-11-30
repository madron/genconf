from unittest import skip
from django.core.urlresolvers import reverse
from django.test import TestCase
from . import factories


class ProjectAdminWizardTest(TestCase):
    def setUp(self):
        factories.UserFactory()
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
        obj = factories.ProjectFactory()
        url = reverse('admin:genconf_projectwizard_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'value="Project name"')

    def test_delete(self):
        obj = factories.ProjectFactory()
        url = reverse('admin:genconf_projectwizard_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @skip('To be fixed')
    def test_add_step2(self):
        url = reverse('admin:genconf_projectwizard_add')
        data = dict()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class ProjectAdminTest(TestCase):
    def setUp(self):
        factories.UserFactory()
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
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        obj = factories.ProjectFactory()
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
        factories.UserFactory()
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
        self.assertEqual(response.status_code, 200)

    def test_configuration(self):
        obj = factories.RouterFactory()
        url = reverse('admin:genconf_router_configuration', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'no aaa new-model')


class VrfAdminTest(TestCase):
    def setUp(self):
        factories.UserFactory()
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
        self.assertEqual(response.status_code, 200)
