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
        model = models.Vlan
        fields = '__all__'
        widgets = dict(
            layer_3_interface=forms.HiddenInput(),
        )

    def __init__(self, *args, **kwargs):
        super(VlanForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            router = self.instance.router
            qs = models.Vrf.objects.filter(router=router)
            if self.instance.layer_3_interface:
                interface = self.instance.layer_3_interface
                self.initial['ipnetwork'] = interface.ipnetwork
                self.initial['vrf'] = interface.vrf.pk
        else:
            qs = models.Vrf.objects.none()
        self.fields['vrf'].queryset = qs

    def clean_vrf(self):
        ipnetwork = self.cleaned_data.get('ipnetwork', None)
        vrf = self.cleaned_data['vrf']
        if ipnetwork and not vrf:
            raise ValidationError(_('This field is required'))
        return self.cleaned_data['vrf']

    def save(self, commit=True):
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
            if ipnetwork:
                interface = models.Layer3Interface.objects.create(
                    ipnetwork=ipnetwork, vrf=vrf)
        self.instance.layer_3_interface = interface
        obj = super(VlanForm, self).save(commit=commit)
        if interface_delete:
            interface_delete.delete()
        return obj


class SubInterfaceForm(forms.ModelForm):
    ipnetwork = NetIPNetworkField(label='Ip network', required=False)
    vrf = forms.ModelChoiceField(models.Vrf.objects.all(), label='Vrf', required=False)

    class Meta:
        model = models.SubInterface
        fields = '__all__'
        widgets = dict(
            layer_3_interface=forms.HiddenInput(),
        )

    def __init__(self, *args, **kwargs):
        super(SubInterfaceForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            router = self.instance.physical_interface.router
            qs = models.Vrf.objects.filter(router=router)
            if self.instance.layer_3_interface:
                interface = self.instance.layer_3_interface
                self.initial['ipnetwork'] = interface.ipnetwork
                self.initial['vrf'] = interface.vrf.pk
        else:
            qs = models.Vrf.objects.none()
        self.fields['vrf'].queryset = qs


    def clean_vrf(self):
        ipnetwork = self.cleaned_data.get('ipnetwork', None)
        vrf = self.cleaned_data['vrf']
        if ipnetwork and not vrf:
            raise ValidationError(_('This field is required'))
        return self.cleaned_data['vrf']

    def save(self, commit=True):
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
            if ipnetwork:
                interface = models.Layer3Interface.objects.create(
                    ipnetwork=ipnetwork, vrf=vrf)
        self.instance.layer_3_interface = interface
        obj = super(SubInterfaceForm, self).save(commit=commit)
        if interface_delete:
            interface_delete.delete()
        return obj
