from django.core import checks
from django.db.models.fields import CharField, GenericIPAddressField
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


class NetIPNetworkField(CharField):
    description = 'netaddr.IPNetwork'

    def __init__(self, protocol='both', *args, **kwargs):
        kwargs['max_length'] = 43
        self.protocol = protocol
        super(NetIPNetworkField, self).__init__(*args, **kwargs)
        self.validators = []

    def _check_blank_and_null_values(self, **kwargs):
        if not getattr(self, 'null', False) and getattr(self, 'blank', False):
            return [
                checks.Error(
                    ('NetIPNetworkField cannot have blank=True if null=False, '
                     'as blank values are stored as nulls.'),
                    hint=None,
                    obj=self,
                    id='fields.E150',
                )
            ]
        return []

    def deconstruct(self):
        name, path, args, kwargs = super(NetIPNetworkField, self).deconstruct()
        if not self.protocol == 'both':
            kwargs['protocol'] = self.protocol
        if kwargs.get("max_length", None) == 43:
            del kwargs['max_length']
        return name, path, args, kwargs

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
