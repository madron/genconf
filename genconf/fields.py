import netaddr
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _


class IPAddressField(CharField):
    default_error_messages = dict(invalid=_('Enter a valid ip address.'))

    def clean(self, value):
        value = super(IPAddressField, self).clean(value)
        value = value.strip()
        if value in self.empty_values:
            return None
        try:
            return netaddr.IPAddress(value)
        except netaddr.AddrFormatError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
