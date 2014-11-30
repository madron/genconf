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
    form_list = [
        ('type', forms.ProjectForm1),
        ('placeholder', forms.ProjectForm2),
    ]

    def process_step(self, form):
        """
        This method is used to postprocess the form data. By default, it
        returns the raw `form.data` dictionary.
        """
        return self.get_form_step_data(form)
