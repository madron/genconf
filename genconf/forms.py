from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from netutils.formfields import NetIPNetworkField
from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectFormStart(ProjectForm):
    class Meta:
        model = models.Project
        fields = ['name']


class PhysicalInterfaceForm(forms.ModelForm):
    class Meta:
        model = models.PhysicalInterface
        fields = '__all__'
        widgets = dict(
            name=forms.TextInput(attrs=dict(size=5)),
            mtu=forms.TextInput(attrs=dict(size=3)),
            duplex=forms.TextInput(attrs=dict(size=3)),
            speed=forms.TextInput(attrs=dict(size=3)),
        )

    def __init__(self, *args, **kwargs):
        super(PhysicalInterfaceForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            router = kwargs['instance'].router
            qs = models.Vlan.objects.filter(router=router)
        else:
            qs = models.Vlan.objects.none()
        self.fields['native_vlan'].queryset = qs


class VlanForm(forms.ModelForm):
    ipnetwork = NetIPNetworkField(label='Ip network', required=False)
    vrf = forms.ModelChoiceField(models.Vrf.objects.all(), label='Vrf', required=False)

    class Meta:
        model = models.SubInterface
        fields = '__all__'
        widgets = dict(
            layer_3_interface=forms.TextInput(attrs=dict(size=5)),
        )

    def __init__(self, *args, **kwargs):
        super(VlanForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.layer_3_interface:
            interface = self.instance.layer_3_interface
            self.initial['ipnetwork'] = interface.ipnetwork
            self.initial['vrf'] = interface.vrf.pk

    def clean_vrf(self):
        ipnetwork = self.cleaned_data['ipnetwork']
        vrf = self.cleaned_data['vrf']
        if ipnetwork and not vrf:
            raise ValidationError(_('This field is required'))
        return self.cleaned_data['vrf']

    def save(self, commit=True):
        if commit:
            interface = self.cleaned_data['layer_3_interface']
            ipnetwork = self.cleaned_data['ipnetwork']
            vrf = self.cleaned_data['vrf']
            interface_delete = None
            if interface:
                if ipnetwork:
                    interface.ipnetwork = ipnetwork
                    interface.vrf = vrf
                    interface.save()
                else:
                    interface_delete = interface
                    interface = None
            else:
                interface = models.Layer3Interface.objects.create(
                    ipnetwork=ipnetwork, vrf=vrf)
            self.instance.layer_3_interface = interface

        vlan = super(VlanForm, self).save(commit=commit)
        if commit and interface_delete:
            interface_delete.delete()
        return vlan
