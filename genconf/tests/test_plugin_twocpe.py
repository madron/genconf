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


class SaveObjectsTest(TestCase):
    def setUp(self):
        from ..plugin import manager
        self.plugin_object = manager.getPluginByName('twocpe').plugin_object

    def test_all_models(self):
        project = factories.ProjectFactory.create(name='Test')
        router = factories.RouterFactory.build(project=project)
        vrf = factories.VrfFactory.build(router=router)
        vlan = factories.VlanFactory.build(router=router, tag=20)
        objects = dict(
            router=[router],
            vrf=[vrf],
            vlan=[vlan],
        )
        self.plugin_object.save_objects(objects)
        self.assertEqual(models.Project.objects.count(), 1)
        self.assertEqual(models.Router.objects.count(), 1)
        self.assertEqual(models.Vrf.objects.count(), 1)
        self.assertEqual(models.Vlan.objects.count(), 1)

    def test_new(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        objects = dict(
            router=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.assertEqual(models.Router.objects.count(), 0)
        self.plugin_object.save_objects(objects)
        self.assertEqual(models.Router.objects.count(), 2)
        # wan1
        router = models.Router.objects.get(name='wan1')
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.project, project)
        self.assertEqual(router.project.id, 1)
        # wan2
        router = models.Router.objects.get(name='wan2')
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.project, project)
        self.assertEqual(router.project.id, 1)

    def test_1_existing(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        router = factories.RouterFactory.build(id=1, project=project)
        factories.VlanFactory.create(router=router, tag=20)
        objects = dict(
            vlan=[
                factories.VlanFactory.build(router=router, tag=1),
                factories.VlanFactory.build(router=router, tag=2),
            ],
        )
        self.assertEqual(models.Vlan.objects.count(), 1)
        self.plugin_object.save_objects(objects)
        self.assertEqual(models.Vlan.objects.count(), 2)
        # vlan
        vlan = models.Vlan.objects.get(tag=1)
        self.assertEqual(vlan.router.id, 1)
        vlan = models.Vlan.objects.get(tag=2)
        self.assertEqual(vlan.router.id, 1)

    def test_2_existing(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project)
        factories.RouterFactory.create(id=2, name='Old', project=project)
        objects = dict(
            router=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.plugin_object.save_objects(objects)
        # wan1
        router = models.Router.objects.get(name='wan1')
        self.assertEqual(router.id, 1)
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.project, project)
        self.assertEqual(router.project.id, 1)
        # wan2
        router = models.Router.objects.get(name='wan2')
        self.assertEqual(router.id, 2)
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.project, project)
        self.assertEqual(router.project.id, 1)

    def test_3_existing(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project)
        factories.RouterFactory.create(id=2, name='Old', project=project)
        factories.RouterFactory.create(id=3, name='One more', project=project)
        objects = dict(
            router=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.assertEqual(models.Router.objects.count(), 3)
        self.plugin_object.save_objects(objects)
        self.assertEqual(models.Router.objects.count(), 2)
        # wan1
        router = models.Router.objects.get(name='wan1')
        self.assertEqual(router.id, 1)
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.project, project)
        self.assertEqual(router.project.id, 1)
        # wan2
        router = models.Router.objects.get(name='wan2')
        self.assertEqual(router.id, 2)
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.project, project)
        self.assertEqual(router.project.id, 1)


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

