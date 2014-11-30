from django.contrib.formtools.wizard.views import SessionWizardView
from django.views.generic import DetailView
from adminwizard.views import AdminWizardView
from . import forms
from . import models


class ConfigurationView(DetailView):
    http_method_names = ['get']
    model = models.Project
    template_name = 'genconf/configuration/configuration.txt'

    def get_context_data(self, **kwargs):
        context = super(ConfigurationView, self).get_context_data(**kwargs)
        context['router'] = kwargs['object']
        return context


class ProjectWizardView(AdminWizardView, SessionWizardView):
    form_list = [forms.ProjectForm1, forms.ProjectForm2]
    template_name = 'adminwizard/change_form.html'
