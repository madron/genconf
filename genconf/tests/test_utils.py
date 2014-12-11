from django.test import TestCase
from .. import factories
from .. import models
from ..utils import (get_physical_interfaces, save_instances, save_project)


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


class SaveProjectTest(TestCase):
    def test_all_models(self):
        project_instance = factories.ProjectFactory.create(name='Test')
        router = factories.RouterFactory.build(project=project_instance)
        vrf = factories.VrfFactory.build(router=router)
        route = factories.RouteFactory.build(vrf=vrf)
        vlan = factories.VlanFactory.build(router=router, tag=20)
        project = dict(
            router=dict(
                wan1=dict(
                    router_instance=router,
                    vrf=[vrf],
                    route=[route],
                    vlan=dict(vlan_20=vlan),
                )
            )
        )
        save_project(project)
        self.assertEqual(models.Project.objects.count(), 1)
        self.assertEqual(models.Router.objects.count(), 1)
        self.assertEqual(models.Vrf.objects.count(), 1)
        self.assertEqual(models.Route.objects.count(), 1)
        self.assertEqual(models.Vlan.objects.count(), 1)

    def test_new(self):
        project_instance = factories.ProjectFactory.create(id=1, name='Test')
        project = dict(
            router=dict(
                wan1=dict(router_instance=factories.RouterFactory.build(project=project_instance, name='wan1')),
                wan2=dict(router_instance=factories.RouterFactory.build(project=project_instance, name='wan2')),
            )
        )
        self.assertEqual(models.Router.objects.count(), 0)
        save_project(project)
        self.assertEqual(models.Router.objects.count(), 2)
        # wan1
        router = models.Router.objects.get(name='wan1')
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.project, project_instance)
        self.assertEqual(router.project.id, 1)
        # wan2
        router = models.Router.objects.get(name='wan2')
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.project, project_instance)
        self.assertEqual(router.project.id, 1)

    def test_1_existing(self):
        project_instance = factories.ProjectFactory.create(id=1, name='Test')
        router = factories.RouterFactory.build(id=1, project=project_instance)
        factories.VlanFactory.create(router=router, tag=20)
        project = dict(
            router=dict(
                wan1=dict(
                    router_instance=router,
                    vlan=dict(
                        vlan_1=factories.VlanFactory.build(router=router, tag=1),
                        default=factories.VlanFactory.build(router=router, tag=2),
                    )
                )
            )
        )
        self.assertEqual(models.Vlan.objects.count(), 1)
        save_project(project)
        self.assertEqual(models.Vlan.objects.count(), 2)
        # vlan
        vlan = models.Vlan.objects.get(tag=1)
        self.assertEqual(vlan.router.id, 1)
        vlan = models.Vlan.objects.get(tag=2)
        self.assertEqual(vlan.router.id, 1)

    def test_2_existing(self):
        project_instance = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project_instance)
        factories.RouterFactory.create(id=2, name='Old', project=project_instance)
        project = dict(
            router=dict(
                wan1=dict(router_instance=factories.RouterFactory.build(project=project_instance, name='wan1')),
                wan2=dict(router_instance=factories.RouterFactory.build(project=project_instance, name='wan2')),
            )
        )
        self.assertEqual(models.Router.objects.count(), 2)
        save_project(project)
        self.assertEqual(models.Router.objects.count(), 2)
        # wan1
        router = models.Router.objects.get(name='wan1')
        self.assertEqual(router.id, 1)
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.project, project_instance)
        self.assertEqual(router.project.id, 1)
        # wan2
        router = models.Router.objects.get(name='wan2')
        self.assertEqual(router.id, 2)
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.project, project_instance)
        self.assertEqual(router.project.id, 1)

    def test_3_existing(self):
        project_instance = factories.ProjectFactory.create(id=1, name='Test')
        factories.RouterFactory.create(id=1, name='Wrong', project=project_instance)
        factories.RouterFactory.create(id=2, name='Old', project=project_instance)
        factories.RouterFactory.create(id=3, name='One more', project=project_instance)
        project = dict(
            router=dict(
                wan1=dict(router_instance=factories.RouterFactory.build(project=project_instance, name='wan1')),
                wan2=dict(router_instance=factories.RouterFactory.build(project=project_instance, name='wan2')),
            )
        )
        self.assertEqual(models.Router.objects.count(), 3)
        save_project(project)
        self.assertEqual(models.Router.objects.count(), 2)
        # wan1
        router = models.Router.objects.get(name='wan1')
        self.assertEqual(router.id, 1)
        self.assertEqual(router.name, 'wan1')
        self.assertEqual(router.project, project_instance)
        self.assertEqual(router.project.id, 1)
        # wan2
        router = models.Router.objects.get(name='wan2')
        self.assertEqual(router.id, 2)
        self.assertEqual(router.name, 'wan2')
        self.assertEqual(router.project, project_instance)
        self.assertEqual(router.project.id, 1)


class GetPhysicalInterfacesTest(TestCase):
    def setUp(self):
        router_instance = factories.RouterFactory.build()
        vlan = factories.VlanFactory.build(router=router_instance)
        self.router = dict(
            router_instance=router_instance,
            vlan=[vlan],
            physicalinterface=[
                factories.PhysicalInterfaceFactory.build(router=router_instance, name='atm0', type='atm', layer=3, native_vlan=vlan),
                factories.PhysicalInterfaceFactory.build(router=router_instance, name='fe0', type='ethernet', layer=3, native_vlan=vlan),
                factories.PhysicalInterfaceFactory.build(router=router_instance, name='fe1', type='ethernet', layer=2, native_vlan=vlan),
            ]
        )

    def test_all(self):
        interfaces = get_physical_interfaces(self.router)
        self.assertEqual(len(interfaces), 3)
        self.assertEqual(interfaces[0].name, 'atm0')
        self.assertEqual(interfaces[1].name, 'fe0')
        self.assertEqual(interfaces[2].name, 'fe1')

    def test_atm(self):
        interfaces = get_physical_interfaces(self.router, type='atm')
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].name, 'atm0')

    def test_ethernet(self):
        interfaces = get_physical_interfaces(self.router, type='ethernet')
        self.assertEqual(len(interfaces), 2)
        self.assertEqual(interfaces[0].name, 'fe0')
        self.assertEqual(interfaces[1].name, 'fe1')

    def test_layer3(self):
        interfaces = get_physical_interfaces(self.router, layer=3)
        self.assertEqual(len(interfaces), 2)
        self.assertEqual(interfaces[0].name, 'atm0')
        self.assertEqual(interfaces[1].name, 'fe0')

    def test_ethernet_layer2(self):
        interfaces = get_physical_interfaces(self.router, type='ethernet', layer=2)
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].name, 'fe1')

    def test_ethernet_layer3(self):
        interfaces = get_physical_interfaces(self.router, type='ethernet', layer=3)
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].name, 'fe0')
