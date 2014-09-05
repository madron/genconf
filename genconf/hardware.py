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
        duplex='auto',
        speed='auto',
        subinterfaces=[]
    ):
        self.name = name
        self.type = type
        self.layers = layers
        self.mtu = mtu
        self.duplex = duplex
        self.speed = speed
        self.subinterfaces = subinterfaces

    @property
    def is_layer2(self):
        return 2 in self.layers

    @property
    def is_layer3(self):
        return 3 in self.layers
