from django.test import TestCase
from .. import factories
from .. import models
from ..utils import save_instances, save_objects


class SaveInstancesTest(TestCase):
    def test_no_instances(self):
        save_instances([])

    def test_mixed_models(self):
        instances = [
            factories.ProjectFactory.build(),
            factories.RouterFactory.build(),
        ]
        self.assertRaises(Exception, save_instances, instances)

    def test_simple_new(self):
        project1 = factories.ProjectFactory.build(name='Project 1')
        project2 = factories.ProjectFactory.build(name='Project 2')
        instances = [project1, project2]
        self.assertEqual(models.Project.objects.count(), 0)
        save_instances(instances, search_fields=['name'])
        self.assertEqual(models.Project.objects.count(), 2)
        # 1
        project = models.Project.objects.get(name='Project 1')
        # 2
        project = models.Project.objects.get(name='Project 2')

    def test_simple_1_existing(self):
        models.Project.objects.create(id=5, name='Old project 9')
        project1 = factories.ProjectFactory.build(name='Project 1')
        project2 = factories.ProjectFactory.build(name='Project 2')
        instances = [project1, project2]
        self.assertEqual(models.Project.objects.count(), 1)
        save_instances(instances, search_fields=['name'])
        self.assertEqual(models.Project.objects.count(), 2)
        # 1
        project = models.Project.objects.get(name='Project 1')
        self.assertEqual(project.id, 5)
        # 2
        project = models.Project.objects.get(name='Project 2')

    def test_simple_2_existing(self):
        models.Project.objects.create(id=5, name='Old project 9')
        models.Project.objects.create(id=6, name='Old project 1')
        project1 = factories.ProjectFactory.build(name='Project 1')
        project2 = factories.ProjectFactory.build(name='Project 2')
        instances = [project1, project2]
        self.assertEqual(models.Project.objects.count(), 2)
        save_instances(instances, search_fields=['name'])
        self.assertEqual(models.Project.objects.count(), 2)
        # 1
        project = models.Project.objects.get(name='Project 1')
        self.assertEqual(project.id, 5)
        # 2
        project = models.Project.objects.get(name='Project 2')
        self.assertEqual(project.id, 6)

    def test_simple_3_existing(self):
        models.Project.objects.create(id=5, name='Old project 9')
        models.Project.objects.create(id=6, name='Old project 1')
        models.Project.objects.create(id=7, name='Old project 5')
        project1 = factories.ProjectFactory.build(name='Project 1')
        project2 = factories.ProjectFactory.build(name='Project 2')
        instances = [project1, project2]
        self.assertEqual(models.Project.objects.count(), 3)
        save_instances(instances, search_fields=['name'])
        self.assertEqual(models.Project.objects.count(), 2)
        # 1
        project = models.Project.objects.get(name='Project 1')
        self.assertEqual(project.id, 5)
        # 2
        project = models.Project.objects.get(name='Project 2')
        self.assertEqual(project.id, 6)

    def test_fk_new(self):
        project1 = models.Project.objects.create(id=1, name='Project 1')
        project2 = models.Project.objects.create(id=2, name='Project 2')
        instances = [
            factories.RouterFactory.build(project=project1, name='Router 1'),
            factories.RouterFactory.build(project=project1, name='Router 2'),
            factories.RouterFactory.build(project=project2, name='Router 3'),
        ]
        self.assertEqual(models.Router.objects.count(), 0)
        save_instances(instances, fixed_fields=['project'], search_fields=['name'])
        self.assertEqual(models.Router.objects.count(), 3)
        # 1
        router = models.Router.objects.get(name='Router 1')
        self.assertEqual(router.project.id, 1)
        # 2
        router = models.Router.objects.get(name='Router 2')
        self.assertEqual(router.project.id, 1)
        # 3
        router = models.Router.objects.get(name='Router 3')
        self.assertEqual(router.project.id, 2)

    def test_fk_1_existing_different_name(self):
        project1 = models.Project.objects.create(id=1, name='Project 1')
        project2 = models.Project.objects.create(id=2, name='Project 2')
        models.Router.objects.create(id=5, project=project1, name='Old router 9')
        instances = [
            factories.RouterFactory.build(project=project1, name='Router 1'),
            factories.RouterFactory.build(project=project1, name='Router 2'),
            factories.RouterFactory.build(project=project2, name='Router 3'),
        ]
        self.assertEqual(models.Router.objects.count(), 1)
        save_instances(instances, fixed_fields=['project'], search_fields=['name'])
        self.assertEqual(models.Router.objects.count(), 3)
        # 1
        router = models.Router.objects.get(name='Router 1')
        self.assertEqual(router.id, 5)
        self.assertEqual(router.project.id, 1)
        # 2
        router = models.Router.objects.get(name='Router 2')
        self.assertEqual(router.project.id, 1)
        # 3
        router = models.Router.objects.get(name='Router 3')
        self.assertEqual(router.project.id, 2)

    def test_fk_1_existing_same_name(self):
        project1 = models.Project.objects.create(id=1, name='Project 1')
        project2 = models.Project.objects.create(id=2, name='Project 2')
        models.Router.objects.create(id=5, project=project1, name='Router 1')
        instances = [
            factories.RouterFactory.build(project=project1, name='Router 1'),
            factories.RouterFactory.build(project=project1, name='Router 2'),
            factories.RouterFactory.build(project=project2, name='Router 3'),
        ]
        self.assertEqual(models.Router.objects.count(), 1)
        save_instances(instances, fixed_fields=['project'], search_fields=['name'])
        self.assertEqual(models.Router.objects.count(), 3)
        # 1
        router = models.Router.objects.get(name='Router 1')
        self.assertEqual(router.id, 5)
        self.assertEqual(router.project.id, 1)
        # 2
        router = models.Router.objects.get(name='Router 2')
        self.assertEqual(router.project.id, 1)
        # 3
        router = models.Router.objects.get(name='Router 3')
        self.assertEqual(router.project.id, 2)

    def test_fk_3_existing(self):
        project1 = models.Project.objects.create(id=1, name='Project 1')
        project2 = models.Project.objects.create(id=2, name='Project 2')
        models.Router.objects.create(id=5, project=project1, name='Router 3')
        models.Router.objects.create(id=3, project=project1, name='Router 1')
        models.Router.objects.create(id=1, project=project1, name='Router 2')
        instances = [
            factories.RouterFactory.build(project=project1, name='Router 1'),
            factories.RouterFactory.build(project=project1, name='Router 2'),
            factories.RouterFactory.build(project=project2, name='Router 3'),
        ]
        self.assertEqual(models.Router.objects.count(), 3)
        save_instances(instances, fixed_fields=['project'], search_fields=['name'])
        self.assertEqual(models.Router.objects.count(), 3)
        # 1
        router = models.Router.objects.get(name='Router 1')
        self.assertEqual(router.id, 3)
        self.assertEqual(router.project.id, 1)
        # 2
        router = models.Router.objects.get(name='Router 2')
        self.assertEqual(router.id, 1)
        self.assertEqual(router.project.id, 1)
        # 3
        router = models.Router.objects.get(name='Router 3')
        self.assertEqual(router.project.id, 2)

    def test_fk_5_existing(self):
        old_project = models.Project.objects.create(id=9, name='Old project')
        project1 = models.Project.objects.create(id=1, name='Project 1')
        project2 = models.Project.objects.create(id=2, name='Project 2')
        models.Router.objects.create(id=5, project=project1, name='Router 1')
        models.Router.objects.create(id=3, project=project2, name='Router 1')
        models.Router.objects.create(id=1, project=project1, name='Router 2')
        models.Router.objects.create(id=2, project=project2, name='Router 2')
        models.Router.objects.create(id=4, project=old_project, name='Router 2')
        instances = [
            factories.RouterFactory.build(project=project1, name='Router 1'),
            factories.RouterFactory.build(project=project1, name='Router 2'),
            factories.RouterFactory.build(project=project2, name='Router 3'),
        ]
        self.assertEqual(models.Router.objects.count(), 5)
        save_instances(instances, fixed_fields=['project'], search_fields=['name'])
        self.assertEqual(models.Router.objects.count(), 4)
        # 1
        router = models.Router.objects.get(project=project1, name='Router 1')
        self.assertEqual(router.id, 5)
        self.assertEqual(router.project.id, 1)
        # 2
        router = models.Router.objects.get(project=project1, name='Router 2')
        self.assertEqual(router.id, 1)
        self.assertEqual(router.project.id, 1)
        # 3
        router = models.Router.objects.get(project=project2, name='Router 3')
        self.assertEqual(router.id, 2)
        self.assertEqual(router.project.id, 2)
        # Old project router
        router = models.Router.objects.get(project=old_project)
        self.assertEqual(router.id, 4)


class SaveObjectsTest(TestCase):
    def test_all_models(self):
        project = factories.ProjectFactory.create(name='Test')
        router = factories.RouterFactory.build(project=project)
        vrf = factories.VrfFactory.build(router=router)
        route = factories.RouteFactory.build(vrf=vrf)
        vlan = factories.VlanFactory.build(router=router, tag=20)
        objects = dict(
            router=[router],
            vrf=[vrf],
            route=[route],
            vlan=[vlan],
        )
        save_objects(objects)
        self.assertEqual(models.Project.objects.count(), 1)
        self.assertEqual(models.Router.objects.count(), 1)
        self.assertEqual(models.Vrf.objects.count(), 1)
        self.assertEqual(models.Route.objects.count(), 1)
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
        save_objects(objects)
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
        save_objects(objects)
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
        save_objects(objects)
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
        save_objects(objects)
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
