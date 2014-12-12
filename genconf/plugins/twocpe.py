import netaddr
from django import forms
from yapsy.IPlugin import IPlugin
from genconf import constants
from netutils import formfields


class Wan1Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    # network = formfields.IPNetworkField()


class Wan2Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    # network = formfields.IPNetworkField()


class FallbackForm(forms.Form):
    network = formfields.IPNetworkField()
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
            # Vrf
            default_vrf = factories.VrfFactory.build(router=router_instance, name='')
            # Vlan
            default_vlan = factories.VlanFactory.build(router=router_instance, tag=1)
            router = dict(
                router_instance=router_instance,
                vrf=dict(default_vrf=default_vrf),
                vlan=dict(default_vlan=default_vlan),
                physicalinterface=[],
                subinterface=[],
                layer3interface=[],
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
        fallback_network = data['fallback']['network']
        # wan1
        router = project['router']['wan1']
        interface_1 = get_physical_interfaces(router, type='ethernet', layer=3)[0]
        vlan = router['vlan']['default_vlan']
        subinterface = factories.SubInterfaceFactory.build(
            name='%s.%d' % (interface_1.name, vlan.tag),
            physical_interface=interface_1, layer=3, vlan=vlan)
        router['subinterface'].append(subinterface)
        ipnetwork = netaddr.IPNetwork(fallback_network.network + 1)
        ipnetwork.prefixlen = fallback_network.prefixlen
        router['layer3interface'].append(factories.Layer3InterfaceFactory.build(
            vlan=None, subinterface=subinterface, ipnetwork=ipnetwork,
            vrf=router['vrf']['default_vrf'], description='Fallback link'
        ))
        # wan2
        router = project['router']['wan2']
        interface_2 = get_physical_interfaces(router, type='ethernet', layer=3)[0]
        vlan = router['vlan']['default_vlan']
        subinterface = factories.SubInterfaceFactory.build(
            name='%s.%d' % (interface_2.name, vlan.tag),
            physical_interface=interface_2, layer=3, vlan=vlan)
        router['subinterface'].append(subinterface)
        ipnetwork = netaddr.IPNetwork(fallback_network.network + 2)
        ipnetwork.prefixlen = fallback_network.prefixlen
        router['layer3interface'].append(factories.Layer3InterfaceFactory.build(
            vlan=None, subinterface=subinterface, ipnetwork=ipnetwork,
            vrf=router['vrf']['default_vrf'], description='Fallback link'
        ))
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
