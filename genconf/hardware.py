from . import routing


class Router(object):
    def __init__(self, name='', vrfs=[], interfaces=()):
        self.name = name
        self.vrfs = vrfs or [routing.Vrf()]
        self.interfaces = interfaces


class PhysicalInterface(object):
    def __init__(
        self,
        name='',
        description='',
        type='ethernet',
        layer=2,
        mtu=1500,
        subinterfaces=[],
    ):
        """
        layer expresses how this interface is used:
        some interfaces can be configured as layer 2 or layer 3

        layer 2 -> switching interface
        layer 3 -> routing interface
        """
        self.name = name
        self.description = description
        self.type = type
        self.layer = layer
        self.mtu = mtu
        self.subinterfaces = subinterfaces

    @property
    def is_layer2(self):
        return self.layer == 2

    @property
    def is_layer3(self):
        return self.layer == 3


class PhysicalInterfaceEthernet(PhysicalInterface):
    def __init__(
        self,
        duplex='auto',
        speed='auto',
        dot1q_mode='access',
        dot1q_encapsulation='802.1q',
        native_vlan=1,
        **kwargs
    ):
        kwargs['type'] = 'ethernet'
        super(PhysicalInterfaceEthernet, self).__init__(**kwargs)
        self.duplex = duplex
        self.speed = speed
        self.dot1q_mode = dot1q_mode
        self.native_vlan = native_vlan
