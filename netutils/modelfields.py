from django.db.models.fields import GenericIPAddressField
from netaddr import IPAddress, IPNetwork
from . import formfields


class NetIPAddressField(GenericIPAddressField):
    description = 'netaddr.IPAddress'

    def to_python(self, value):
        if isinstance(value, IPAddress) or value is None:
            return value
        return IPAddress(value)

    def get_prep_value(self, value):
        ' catches value right before sending to db '
        if value:
            return str(value)
        return None

    def formfield(self, **kwargs):
        defaults = dict(form_class=formfields.NetIPAddressField)
        defaults.update(kwargs)
        return super(NetIPAddressField, self).formfield(**defaults)


class NetIPNetworkField(GenericIPAddressField):
    description = 'netaddr.IPNetwork'

    def to_python(self, value):
        if isinstance(value, IPNetwork) or value is None:
            return value
        return IPNetwork(value)

    def get_prep_value(self, value):
        ' catches value right before sending to db '
        if value:
            return str(value)
        return None

    def formfield(self, **kwargs):
        defaults = dict(form_class=formfields.NetIPNetworkField)
        defaults.update(kwargs)
        return super(NetIPNetworkField, self).formfield(**defaults)
