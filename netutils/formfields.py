import netaddr
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _


class NetIPAddressField(CharField):
    default_error_messages = dict(
        invalid=_('Enter a valid ip address.'),
        notipv4=_('Enter a valid ipv4 address.'),
        notipv6=_('Enter a valid ipv6 address.'),
    )

    def __init__(self, protocol='both', *args, **kwargs):
        if protocol not in ('both', 'ipv4', 'ipv6'):
            msg = "Unknown protocol: only 'both', 'ipv4' and 'ipv6' are allowed."
            raise ValueError(msg)
        self.protocol = protocol
        super(NetIPAddressField, self).__init__(*args, **kwargs)


    def clean(self, value):
        value = super(NetIPAddressField, self).clean(value)
        value = value.strip()
        if value in self.empty_values:
            return None
        try:
            value = netaddr.IPAddress(value)
        except netaddr.AddrFormatError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        if self.protocol == 'ipv4' and not value.version == 4:
            raise ValidationError(self.error_messages['notipv4'], code='notipv4')
        if self.protocol == 'ipv6' and not value.version == 6:
            raise ValidationError(self.error_messages['notipv6'], code='notipv6')
        return value


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
