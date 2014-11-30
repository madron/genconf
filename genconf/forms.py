from django import forms
from django.utils.translation import ugettext as _
from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectForm1(ProjectForm):
    class Meta:
        model = models.Project
        fields = ['name', 'type']


class ProjectForm2(forms.Form):
    " This is just a placeholder"
    pass
