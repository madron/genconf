from netaddr import IPNetwork


class LanConfig(dict):
    def __init__(self, *args, **kwargs):
        super(LanConfig, self).__init__(*args, **kwargs)
        for name, value in self.iteritems():
            self[name] = value

    def __setitem__(self, name, value):
        if hasattr(self, 'clean_%s' % name):
            value = getattr(self, 'clean_%s' % name)(value)
        super(LanConfig, self).__setitem__(name, value)

    def clean_subnet(self, value):
        return IPNetwork(value)
