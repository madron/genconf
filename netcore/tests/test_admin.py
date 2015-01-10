from django.core.urlresolvers import reverse
from django.test import TestCase
from . import factories


class BrasAdminTest(TestCase):
    def setUp(self):
        factories.UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:netcore_bras_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:netcore_bras_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        obj = factories.BrasFactory(name='Bras name')
        url = reverse('admin:netcore_bras_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'value="Bras name"')

    def test_detail_loopback_vrf(self):
        bras_1 = factories.BrasFactory(name='bras_1')
        bras_2 = factories.BrasFactory(name='bras_2')
        factories.VrfFactory(bras=bras_1, number=1, name='VRF_1')
        factories.VrfFactory(bras=bras_2, number=2, name='VRF_2')
        factories.LoopbackFactory(bras=bras_1, number=1, vrf=None)
        url = reverse('admin:netcore_bras_change', args=(bras_1.pk,))
        response = self.client.get(url)
        self.assertContains(response, 'VRF_1')
        self.assertNotContains(response, 'VRF_2')

    def test_delete(self):
        obj = factories.BrasFactory()
        url = reverse('admin:netcore_bras_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class VrfAdminTest(TestCase):
    def setUp(self):
        factories.UserFactory()
        self.assertTrue(self.client.login(username='test', password='pass'))
        self.list = reverse('admin:netcore_vrf_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:netcore_vrf_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        obj = factories.VrfFactory(number=1)
        url = reverse('admin:netcore_vrf_change', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        obj = factories.VrfFactory(number=1)
        url = reverse('admin:netcore_vrf_delete', args=(obj.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
