import json
import netaddr
from . import hardware
from . import routing
from . import serializers


class RouterSerializer(serializers.DictSerializer):
    _classes = (
        ('ipaddress', netaddr.IPAddress),
        ('ipnetwork', netaddr.IPNetwork),
        ('route', routing.Route),
        ('vrf', routing.Vrf),
        ('bgpneighbour', routing.BgpNeighbour),
        ('bgp', routing.Bgp),
        ('layer2interface', routing.Layer2Interface),
        ('layer3interface', routing.Layer3Interface),
        ('vlan', routing.Vlan),
        ('subinterface', routing.SubInterface),
        ('subinterfaceethernet', routing.SubInterfaceEthernet),
        ('subinterfaceatm', routing.SubInterfaceAtm),
        ('router', hardware.Router),
        ('physicalinterface', hardware.PhysicalInterface),
        ('physicalinterfaceethernet', hardware.PhysicalInterfaceEthernet),
    )

    def dump_ipaddress(self, obj):
        return str(obj)

    def dump_ipnetwork(self, obj):
        return str(obj)


def router_dump(router):
    return json.dumps(
        RouterSerializer().dump(router),
        sort_keys=True,
        indent=4,
    )


def router_load(data):
    return RouterSerializer().load(json.loads(data))
