class Router(object):
    def __init__(self, name='', interfaces=(), vrfs=[]):
        self.name = name
        self.interfaces = interfaces
        self.vrfs = vrfs or [Vrf()]


class PhysicalInterface(object):
    def __init__(
        self,
        name='',
        type='ethernet',
        layers=[],
        mtu=1500,
    ):
        self.name = name
        self.type = type
        self.layers = layers
        self.mtu = mtu

    @property
    def is_layer2(self):
        return 2 in self.layers

    @property
    def is_layer3(self):
        return 3 in self.layers


class PhysicalInterfaceEthernet(PhysicalInterface):
    def __init__(
        self,
        duplex='auto',
        speed='auto',
        dot1q_mode='access',
        native_vlan=1,
        **kwargs
    ):
        kwargs['type'] = 'ethernet'
        super(PhysicalInterfaceEthernet, self).__init__(**kwargs)
        self.duplex = duplex
        self.speed = speed
        self.dot1q_mode = dot1q_mode
        self.native_vlan = native_vlan
