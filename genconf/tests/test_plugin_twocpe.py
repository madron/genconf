from django.test import TestCase
from .. import factories
from .. import models
from ..plugins import twocpe


class GetObjectsTest(TestCase):
    def setUp(self):
        from ..plugin import manager
        self.plugin_object = manager.getPluginByName('twocpe').plugin_object
        self.project = factories.ProjectFactory(name='Test')

    def test_get_objects(self):
        data = dict(
            wan1=dict(access_type='ethernet', router='c1841'),
            wan2=dict(access_type='adsl', router='c1801'),
        )
        objects = self.plugin_object.get_objects(self.project, data)
        #
        # Router wan1
        #
        router = objects['router'][0]
        self.assertEqual(router.project, self.project)
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.model, 'c1841')
        # Vlan
        vlan = objects['vlan'][0]
        self.assertEqual(vlan.tag, 1)
        self.assertEqual(vlan.router, router)
        # PhysicalInterface
        interface = objects['physicalinterface'][0]
        self.assertEqual(interface.router, router)
        self.assertEqual(interface.name, 'fe0/0')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 3)
        interface = objects['physicalinterface'][1]
        self.assertEqual(interface.router, router)
        self.assertEqual(interface.name, 'fe0/1')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 3)
        #
        # Router wan2
        #
        router = objects['router'][1]
        self.assertEqual(router.project, self.project)
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.model, 'c1801')
        # Vlan
        vlan = objects['vlan'][1]
        self.assertEqual(vlan.tag, 1)
        self.assertEqual(vlan.router, router)
        # PhisicalInterface
        interface = objects['physicalinterface'][2]
        self.assertEqual(interface.router, router)
        self.assertEqual(interface.name, 'atm0')
        self.assertEqual(interface.type, 'atm')
        self.assertEqual(interface.layer, 3)
        interface = objects['physicalinterface'][3]
        self.assertEqual(interface.router, router)
        self.assertEqual(interface.name, 'fe0')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 3)
        interface = objects['physicalinterface'][11]
        self.assertEqual(interface.router, router)
        self.assertEqual(interface.name, 'fe8')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 2)


class SaveTest(TestCase):
    def setUp(self):
        from ..plugin import manager
        self.plugin_object = manager.getPluginByName('twocpe').plugin_object

    def test_save(self):
        project = factories.ProjectFactory.create(name='Test')
        data = dict(
            wan1=dict(access_type='ethernet', router='c1841'),
            wan2=dict(access_type='adsl', router='c1801'),
        )
        self.plugin_object.save(project, data)
        self.assertEqual(models.Project.objects.count(), 1)
        self.assertEqual(models.Router.objects.count(), 2)

