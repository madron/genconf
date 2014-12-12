import netaddr
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _


class NetIPAddressField(CharField):
    default_error_messages = dict(invalid=_('Enter a valid ip address.'))

    def __init__(self, protocol='both', *args, **kwargs):
        self.protocol = protocol
        super(NetIPAddressField, self).__init__(*args, **kwargs)


    def clean(self, value):
        value = super(NetIPAddressField, self).clean(value)
        value = value.strip()
        if value in self.empty_values:
            return None
        try:
            return netaddr.IPAddress(value)
        except netaddr.AddrFormatError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')


class NetIPNetworkField(CharField):
    default_error_messages = dict(invalid=_('Enter a valid ip network (e.g.: 192.168.1.1/24).'))

    def clean(self, value):
        value = super(NetIPNetworkField, self).clean(value)
        value = value.strip()
        if value in self.empty_values:
            return None
        try:
            return netaddr.IPNetwork(value)
        except netaddr.AddrFormatError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
