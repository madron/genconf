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
