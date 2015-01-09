from django import forms
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
