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


class TwoCpe(IPlugin):
    form_list = [
        ('wan1', Wan1Form),
        ('wan2', Wan2Form),
    ]

    def get_objects(self, project, data):
        from genconf import factories
        from genconf import hardware
        objects = dict(
            router=[],
            vlan=[],
            physicalinterface=[],
        )
        for name, wan in [('wan1', data['wan1']), ('wan2', data['wan2'])]:
            # Router
            router = factories.RouterFactory.build(
                project=project,
                name=name,
                model=wan['router']
            )
            objects['router'].append(router)
            # Vlan
            vlan = factories.VlanFactory.build(
                router=router,
                tag=1,
            )
            objects['vlan'].append(vlan)
            # PhysicalInterface
            router_type = hardware.ROUTER_TYPE[router.model]
            for interface in router_type['interfaces']:
                pif = factories.PhysicalInterfaceFactory.build(
                    router=router,
                    name=interface['name'],
                    type=interface['type'],
                    layer=interface['layer'],
                    native_vlan=vlan,
                )
                objects['physicalinterface'].append(pif)
        return objects

    def save(self, project, data):
        from genconf.utils import save_objects
        objects = self.get_objects(project, data)
        save_objects(objects)
