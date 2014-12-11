from django import forms
from yapsy.IPlugin import IPlugin
from genconf import constants
from genconf import fields


class Wan1Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    network = fields.IPNetworkField()


class Wan2Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    network = fields.IPNetworkField()


class FallbackForm(forms.Form):
    network = fields.IPNetworkField()
    password = forms.CharField()


class TwoCpe(IPlugin):
    form_list = [
        ('wan1', Wan1Form),
        ('wan2', Wan2Form),
        ('fallback', FallbackForm),
    ]

    def get_project(self, project_instance, data):
        from genconf import factories
        from genconf import hardware
        from genconf.utils import get_physical_interfaces
        project = dict(
            router=dict(
            ),
            physicallink=[],
        )
        router = dict()
        for name, wan in [('wan1', data['wan1']), ('wan2', data['wan2'])]:
            # Router
            router_instance = factories.RouterFactory.build(
                project=project_instance,
                name=name,
                model=wan['router']
            )
            # Vlan
            default_vlan = factories.VlanFactory.build(router=router_instance, tag=1)
            router = dict(
                router_instance=router_instance,
                vlan=dict(default_vlan=default_vlan),
                physicalinterface=[],
                subinterface=[],
            )
            # PhysicalInterface
            router_type = hardware.ROUTER_TYPE[router_instance.model]
            for interface in router_type['interfaces']:
                pif = factories.PhysicalInterfaceFactory.build(
                    router=router_instance,
                    name=interface['name'],
                    type=interface['type'],
                    layer=interface['layer'],
                    native_vlan=default_vlan,
                )
                router['physicalinterface'].append(pif)
            project['router'][name] = router
        ### Fallback
        # wan1
        router = project['router']['wan1']
        interface_1 = get_physical_interfaces(router, type='ethernet', layer=3)[0]
        subinterface = factories.SubInterfaceFactory.build(
            physical_interface=interface_1, layer=3, vlan=router['vlan']['default_vlan'])
        router['subinterface'].append(subinterface)
        # wan2
        router = project['router']['wan2']
        interface_2 = get_physical_interfaces(router, type='ethernet', layer=3)[0]
        subinterface = factories.SubInterfaceFactory.build(
            physical_interface=interface_2, layer=3, vlan=router['vlan']['default_vlan'])
        router['subinterface'].append(subinterface)
        # PhysicalLink
        project['physicallink'].append(factories.PhysicalLinkFactory.build(
                project=project_instance,
                router_interface_1=interface_1,
                router_interface_2=interface_2,
        ))
        return project

    def save(self, project_instance, data):
        from genconf.utils import save_project
        project = self.get_project(project_instance, data)
        save_project(project)
