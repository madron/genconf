from django.contrib.formtools.wizard.views import SessionWizardView
from django.views.generic import DetailView
from adminwizard.views import AdminWizardView
from . import forms
from . import models
from . import utils


class ConfigurationView(DetailView):
    http_method_names = ['get']
    model = models.Project
    template_name = 'genconf/configuration/configuration.txt'

    def get_context_data(self, **kwargs):
        context = super(ConfigurationView, self).get_context_data(**kwargs)
        context['router'] = utils.router_load(kwargs['object'].configuration)
        return context


class ProjectWizardView(AdminWizardView, SessionWizardView):
    form_list = [forms.ProjectForm1, forms.ProjectForm2]
    template_name = 'genconf/project/change_form.html'
