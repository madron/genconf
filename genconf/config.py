from netaddr import IPNetwork


class LanConfig(object):
    def __init__(self, description='', subnet=None):
        self.description = description
        self.subnet = subnet

    def set_subnet(self, value):
        self._subnet = IPNetwork(value) if value else None

    def get_subnet(self):
        return self._subnet

    subnet = property(get_subnet, set_subnet)
