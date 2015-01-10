from django import forms
from . import models


class LoopbackForm(forms.ModelForm):
    class Meta:
        model = models.Loopback
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LoopbackForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            bras = self.instance.bras
            qs = models.Vrf.objects.filter(bras=bras)
        else:
            qs = models.Vrf.objects.none()
        self.fields['vrf'].queryset = qs
