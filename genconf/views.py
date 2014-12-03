from collections import OrderedDict
from django.contrib.formtools.wizard.storage import get_storage
from django.contrib.formtools.wizard.views import SessionWizardView, StepsHelper
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

    def update_form_list(self, plugin_type):
        from .plugin import manager
        plugin_object = manager.getPluginByName(plugin_type).plugin_object
        form_list = list(self.form_list.iteritems())[0:1]
        self.form_list = OrderedDict(form_list + plugin_object.form_list)

    def dispatch(self, request, *args, **kwargs):
        self.prefix = self.get_prefix(*args, **kwargs)
        self.storage = get_storage(self.storage_name, self.prefix, request,
            getattr(self, 'file_storage', None))
        data = self.storage.get_step_data('type')
        if data:
            plugin_type = data['type-type']
            self.update_form_list(plugin_type)
        elif 'type-type' in request.POST:
            plugin_type = request.POST['type-type']
            self.update_form_list(plugin_type)
        return super(ProjectWizardView, self).dispatch(request, *args, **kwargs)
