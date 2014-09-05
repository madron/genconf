class Route(object):
    def __init__(self, name='', network=None, next_hop=None, metric=1, tag=None):
        self.name = name
        self.network = network
        self.next_hop = next_hop
        self.metric = metric
        self.tag = tag


class Vrf(object):
    def __init__(self, name=None, default_gateway=None, static_routes=[]):
        self.name = name or None
        self.default_gateway = default_gateway
        self.static_routes = static_routes

    @property
    def is_global(self):
        return not self.name


class Layer2Interface(object):
    def __init__(
        self,
        description='',
        mode='access',
        vlan=1,
        allowed_vlans='all',
        encapsulation='802.1q',
        stp_bpdu_filter=True,
        stp_portfast=True,
        broadcast_level_percentage=5,
    ):
        self.description=description
        self.mode=mode
        self.vlan=vlan
        self.allowed_vlans=allowed_vlans
        self.encapsulation=encapsulation
        self.stp_bpdu_filter=stp_bpdu_filter
        self.stp_portfast=stp_portfast
        self.broadcast_level_percentage=broadcast_level_percentage


class Layer3Interface(object):
    def __init__(
        self,
        description='',
        ipnetwork=None,
        vrf=None,
    ):
        self.description = description
        self.ipnetwork = ipnetwork
        self.vrf = vrf or Vrf()


class SubInterface(Layer3Interface):
    def __init__(self, name='', type='ethernet', **kwargs):
        super(SubInterface, self).__init__(**kwargs)
        self.name = name
        self.type = type


class SubInterfaceEthernet(SubInterface):
    def __init__(self, encapsulation='802.1q', vlan=1, native=False, **kwargs):
        # name = '%s.%d' % (name, vlan)
        kwargs['type'] = 'ethernet'
        super(SubInterfaceEthernet, self).__init__(**kwargs)
        self.encapsulation = encapsulation
        self.vlan = vlan
        self.native = native


class SubInterfaceAtm(SubInterface):
    def __init__(
        self,
        link='point-to-point',
        pvc='8/35',
        pvc_encapsulation='pppoa',
        pvc_mux='vc-mux',
        pvc_dialer_pool_number=1,
        **kwargs
    ):
        # name = '%s.%d' % (name, vlan)
        kwargs['type'] = 'atm'
        super(SubInterfaceAtm, self).__init__(**kwargs)
        self.link = link
        self.pvc = pvc
        self.pvc_encapsulation = pvc_encapsulation
        self.pvc_mux = pvc_mux
        self.pvc_dialer_pool_number = pvc_dialer_pool_number
