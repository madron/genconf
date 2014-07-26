class PhysicalInterface(object):
    def __init__(self, name='', type='', layers=()):
        self.name = name
        self.type = type
        self.layers = layers

    @property
    def is_layer2(self):
        return 2 in self.layers

    @property
    def is_layer3(self):
        return 3 in self.layers
