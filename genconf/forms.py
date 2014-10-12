from django import forms
from django.utils.translation import ugettext as _
from . import models
from . import utils


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'

    def clean_configuration(self):
        configuration = self.cleaned_data.get('configuration')
        if not configuration:
            return ''
        try:
            utils.router_load(configuration)
        except ValueError:
            raise forms.ValidationError('Invalid configuration.')
        return configuration
