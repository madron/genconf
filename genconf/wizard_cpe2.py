import netaddr
from django import forms
from netutils import formfields
from . import constants
from . import factories
from . import hardware
from .forms import ProjectFormStart
from .utils import get_physical_interfaces
from .utils import save_project
from .wizard_base import BaseProjectWizardView


class Wan1Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    # network = formfields.NetIPNetworkField()


class Wan2Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)
    router = forms.ChoiceField(choices=constants.ROUTER_TYPE_CHOICES)
    # network = formfields.NetIPNetworkField()


class FallbackForm(forms.Form):
    network = formfields.NetIPNetworkField()
    password = forms.CharField()


class ProjectWizardView(BaseProjectWizardView):
    wizard_name = 'cpe2'
    form_list = [
        ('start', ProjectFormStart),
        ('wan1', Wan1Form),
        ('wan2', Wan2Form),
        ('fallback', FallbackForm),
    ]

    def get_project(self, project_instance, data):
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
        vlan = router['vlan']['default_vlan']
        interface_1 = get_physical_interfaces(router, type='ethernet', layer=3)[0]
        ipnetwork = netaddr.IPNetwork(fallback_network.network + 1)
        ipnetwork.prefixlen = fallback_network.prefixlen
        layer_3_interface = factories.Layer3InterfaceFactory.build(
            ipnetwork=ipnetwork, vrf=router['vrf']['default_vrf'],
            description='Fallback link'
        )
        router['layer3interface'].append(layer_3_interface)
        subinterface = factories.SubInterfaceFactory.build(
            name='%s.%d' % (interface_1.name, vlan.tag),
            physical_interface=interface_1, layer=3, vlan=vlan,
            layer_3_interface=layer_3_interface)
        router['subinterface'].append(subinterface)
        # wan2
        router = project['router']['wan2']
        vlan = router['vlan']['default_vlan']
        interface_2 = get_physical_interfaces(router, type='ethernet', layer=3)[0]
        ipnetwork = netaddr.IPNetwork(fallback_network.network + 2)
        ipnetwork.prefixlen = fallback_network.prefixlen
        layer_3_interface = factories.Layer3InterfaceFactory.build(
            ipnetwork=ipnetwork, vrf=router['vrf']['default_vrf'],
            description='Fallback link'
        )
        router['layer3interface'].append(layer_3_interface)
        subinterface = factories.SubInterfaceFactory.build(
            name='%s.%d' % (interface_2.name, vlan.tag),
            physical_interface=interface_2, layer=3, vlan=vlan,
            layer_3_interface=layer_3_interface)
        router['subinterface'].append(subinterface)
        ipnetwork = netaddr.IPNetwork(fallback_network.network + 2)
        ipnetwork.prefixlen = fallback_network.prefixlen
        # PhysicalLink
        project['physicallink'].append(factories.PhysicalLinkFactory.build(
                project=project_instance,
                router_interface_1=interface_1,
                router_interface_2=interface_2,
        ))
        return project

    def save_project(self, project_instance, data):
        project = self.get_project(project_instance, data)
        save_project(project)
