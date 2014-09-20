class Route(object):
    def __init__(self, name='', network=None, next_hop=None, metric=1, tag=None):
        self.name = name
        self.network = network
        self.next_hop = next_hop
        self.metric = metric
        self.tag = tag


class Vrf(object):
    def __init__(self, name='', default_gateway=None, static_routes=[], bgp=None):
        self.name = name or ''
        self.default_gateway = default_gateway
        self.static_routes = static_routes
        self.bgp = bgp

    @property
    def is_global(self):
        return not self.name


class BgpNeighbour(object):
    def __init__(self):
        self.ip = ip
        self.autonomous_system = autonomous_system
        ### self.direction = 'in' or 'out'
        # self.prefix_lists(direction, network, le)
        # self.routemaps(direction, network, match, local_preference, metric, tag, used_for_default_route=False)
        self.default_originate = False
        self.update_source_interface = ''
        self.ebgp_multihop = 1


class Bgp(object):
    def __init__(self):
        return
        # autonomous_system,
        # router_id,
        # neighbours = []
        # networks = []
        # redistribute_static = False
        # redistribute_connected = False
        # version = 4
        # timer_1 = 10
        # timer_2 = 30
        # maximum_path = 1


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
        vrf_name='',
    ):
        self.description = description
        self.ipnetwork = ipnetwork
        self.vrf_name = vrf_name


class Vlan(object):
    def __init__(self, tag=1, layer_3_interface=None, description='', notes=''):
        self.tag = tag
        self.layer_3_interface = layer_3_interface
        self.description = description
        self.notes = notes

    def get_parent(self):
        raise Exception('To be implemented')


class SubInterface(object):
    def __init__(self, name='', layer_3_interface=None, description='', notes=''):
        """
        layer_3_interface must be None if used as layer 2 in SubInterfaceEthernet
        In all other cases is mandatory
        """
        self.name = name
        self.layer_3_interface = layer_3_interface
        self.description = description
        self.notes = notes

    def get_parent(self):
        raise Exception('To be implemented')


class SubInterfaceEthernet(SubInterface):
    def __init__(self, layer=3, vlan=1, **kwargs):
        """
        layer 3 -> subinterface with ip
        layer 2 -> bridged to vlan
        """
        # name = '%s.%d' % (name, vlan)
        super(SubInterfaceEthernet, self).__init__(**kwargs)
        self.layer = layer
        self.vlan = vlan


class SubInterfaceAtm(SubInterface):
    def __init__(
        self,
        link='point-to-point',
        pvc_vp='8',
        pvc_vc='35',
        pvc_encapsulation='pppoa',
        pvc_mux='vc-mux',
        pvc_dialer_pool_number=1,
        **kwargs
    ):
        # name = '%s.%d' % (name, vlan)
        super(SubInterfaceAtm, self).__init__(**kwargs)
        self.link = link
        self.pvc_vp = pvc_vp
        self.pvc_vc = pvc_vc
        self.pvc_encapsulation = pvc_encapsulation
        self.pvc_mux = pvc_mux
        self.pvc_dialer_pool_number = pvc_dialer_pool_number
