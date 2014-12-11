import netaddr
from django.test import TestCase
from .. import factories
from .. import models
from ..plugins import twocpe


class GetProjectTest(TestCase):
    def setUp(self):
        from ..plugin import manager
        self.plugin_object = manager.getPluginByName('twocpe').plugin_object
        self.project_instance = factories.ProjectFactory(name='Test')

    def test_get_project(self):
        data = dict(
            wan1=dict(access_type='ethernet', router='c1841'),
            wan2=dict(access_type='adsl', router='c1801'),
            fallback=dict(network=netaddr.IPNetwork('192.168.100.1/30')),
        )
        project = self.plugin_object.get_project(self.project_instance, data)
        # Expected structure
        # project = {
        #     'physicallink': [],
        #     'router': {
        #         'wan1': {
        #             'physicalinterface': [
        #                 <PhysicalInterface: wan1 fe0/0>,
        #                 <PhysicalInterface: wan1 fe0/1>,
        #             ],
        #             'router': <Router: wan1>,
        #             'subinterface': [],
        #             'vlan': {'default_vlan': <Vlan: 1>},
        #         },
        #         'wan2': {
        #             'physicalinterface': [
        #                 <PhysicalInterface: wan2 atm0>,
        #                 <PhysicalInterface: wan2 fe0>,
        #                 <PhysicalInterface: wan2 fe1>,
        #             ],
        #             'router': <Router: wan2>,
        #             'subinterface': [],
        #             'vlan': {'default_vlan': <Vlan: 1>},
        #         },
        #     },
        # }

        #
        # Router wan1
        #
        router = project['router']['wan1']
        router_instance = router['router_instance']
        self.assertEqual(router_instance.project, self.project_instance)
        self.assertEqual(router_instance.name, 'wan1')
        self.assertEqual(router_instance.model, 'c1841')
        # Vlan
        self.assertEqual(len(router['vlan']), 1)
        vlan = router['vlan']['default_vlan']
        self.assertEqual(vlan.tag, 1)
        self.assertEqual(vlan.router, router_instance)
        # PhysicalInterface
        self.assertEqual(len(router['physicalinterface']), 2)
        interface = router['physicalinterface'][0]
        self.assertEqual(interface.router, router_instance)
        self.assertEqual(interface.name, 'fe0/0')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 3)
        interface = router['physicalinterface'][1]
        self.assertEqual(interface.router, router_instance)
        self.assertEqual(interface.name, 'fe0/1')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 3)
        # SubInterface
        self.assertEqual(len(router['subinterface']), 1)
        interface = router['subinterface'][0]
        self.assertEqual(interface.physical_interface.router.name, 'wan1')
        self.assertEqual(interface.physical_interface.name, 'fe0/0')
        #
        # Router wan2
        #
        router = project['router']['wan2']
        router_instance = router['router_instance']
        self.assertEqual(router_instance.project, self.project_instance)
        self.assertEqual(router_instance.name, 'wan2')
        self.assertEqual(router_instance.model, 'c1801')
        # Vlan
        self.assertEqual(len(router['vlan']), 1)
        vlan = router['vlan']['default_vlan']
        self.assertEqual(vlan.tag, 1)
        self.assertEqual(vlan.router, router_instance)
        # PhisicalInterface
        self.assertEqual(len(router['physicalinterface']), 10)
        interface = router['physicalinterface'][0]
        self.assertEqual(interface.router, router_instance)
        self.assertEqual(interface.name, 'atm0')
        self.assertEqual(interface.type, 'atm')
        self.assertEqual(interface.layer, 3)
        interface = router['physicalinterface'][1]
        self.assertEqual(interface.router, router_instance)
        self.assertEqual(interface.name, 'fe0')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 3)
        interface = router['physicalinterface'][9]
        self.assertEqual(interface.router, router_instance)
        self.assertEqual(interface.name, 'fe8')
        self.assertEqual(interface.type, 'ethernet')
        self.assertEqual(interface.layer, 2)
        # SubInterface
        self.assertEqual(len(router['subinterface']), 1)
        interface = router['subinterface'][0]
        self.assertEqual(interface.physical_interface.router.name, 'wan2')
        self.assertEqual(interface.physical_interface.name, 'fe0')
        #
        # Links
        #
        self.assertEqual(len(project['physicallink']), 1)
        link = project['physicallink'][0]
        self.assertEqual(link.router_interface_1.router.name, 'wan1')
        self.assertEqual(link.router_interface_1.name, 'fe0/0')
        self.assertEqual(link.router_interface_2.router.name, 'wan2')
        self.assertEqual(link.router_interface_2.name, 'fe0')


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
        self.assertEqual(models.Vlan.objects.count(), 2)
        self.assertEqual(models.PhysicalInterface.objects.count(), 12)
        self.assertEqual(models.SubInterface.objects.count(), 2)
        self.assertEqual(models.PhysicalLink.objects.count(), 1)
