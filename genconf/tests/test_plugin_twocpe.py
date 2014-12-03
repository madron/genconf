from django.test import TestCase
from .. import factories
from .. import models


class ProjectModelTest(TestCase):
    def test_str(self):
        project = factories.ProjectFactory(name='Test')
        self.assertEqual(str(project), 'Test')


class TwoCpePluginTest(TestCase):
    def setUp(self):
        from ..plugin import manager
        self.plugin_object = manager.getPluginByName('twocpe').plugin_object

    def test_save_objects_new(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        objects = dict(
            routers=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.assertEqual(models.Router.objects.count(), 0)
        self.plugin_object.save_objects(project, objects)
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

    def test_save_objects_update(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project)
        factories.RouterFactory.create(id=2, name='Old', project=project)
        objects = dict(
            routers=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.plugin_object.save_objects(project, objects)
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

    def test_save_objects_update_one_more(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project)
        factories.RouterFactory.create(id=2, name='Old', project=project)
        factories.RouterFactory.create(id=3, name='One more', project=project)
        objects = dict(
            routers=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.assertEqual(models.Router.objects.count(), 3)
        self.plugin_object.save_objects(project, objects)
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

    def test_save_objects_update_one_less(self):
        project = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project)
        objects = dict(
            routers=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )
        self.assertEqual(models.Router.objects.count(), 1)
        self.plugin_object.save_objects(project, objects)
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

    def test_get_objects(self):
        project = factories.ProjectFactory(name='Test')
        data = dict(
            wan1=dict(access_type='ethernet'),
            wan2=dict(access_type='adsl'),
        )
        objects = self.plugin_object.get_objects(project, data)
        # Router wan1
        router = objects['routers'][0]
        self.assertEqual(router.project, project)
        self.assertEqual(router.name, 'wan1')
        # Router wan2
        router = objects['routers'][1]
        self.assertEqual(router.project, project)
        self.assertEqual(router.name, 'wan2')
