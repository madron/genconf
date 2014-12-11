import json
from collections import OrderedDict
from django.contrib.formtools.wizard.storage import get_storage
from django.contrib.formtools.wizard.views import SessionWizardView
from django.views.generic import DetailView
from adminwizard.views import AdminWizardView
from . import forms
from . import models
from . import serializers


class ConfigurationView(DetailView):
    http_method_names = ['get']
    model = models.Router
    template_name = 'genconf/configuration/configuration.txt'


class ProjectWizardView(AdminWizardView, SessionWizardView):
    form_list = [
        ('start', forms.ProjectForm1),
        ('placeholder', forms.ProjectForm2),
    ]

    def update_form_list(self, plugin_type):
        from .plugin import manager
        plugin_object = manager.getPluginByName(plugin_type).plugin_object
        form_list = list(self.form_list.iteritems())[0:1]
        self.form_list = OrderedDict(form_list + plugin_object.form_list)
        self.plugin_object = plugin_object

    def get_form_initial(self, step):
        if step == 'start':
            return super(ProjectWizardView, self).get_form_initial(step)
        return self.initial_dict.get(step, {})

    def dispatch(self, request, *args, **kwargs):
        # initial_dict
        if not self.initial_dict:
            object_id = kwargs.get('object_id')
            if object_id:
                project = models.Project.objects.get(pk=object_id)
                if project.configuration:
                    self.initial_dict = json.loads(project.configuration)
        # form_list
        self.prefix = self.get_prefix(*args, **kwargs)
        self.storage = get_storage(self.storage_name, self.prefix, request,
            getattr(self, 'file_storage', None))
        data = self.storage.get_step_data('start')
        if data:
            plugin_type = data['start-type']
            self.update_form_list(plugin_type)
        elif 'start-type' in request.POST:
            plugin_type = request.POST['start-type']
            self.update_form_list(plugin_type)
        return super(ProjectWizardView, self).dispatch(request, *args, **kwargs)

    def save(self, form):
        data = OrderedDict()
        for step in self.form_list.keys():
            if not step == 'start':
                data[step] = self.get_cleaned_data_for_step(step)
        project = form.save(commit=False)
        project.configuration = json.dumps(data, indent=4, cls=serializers.ProjectEncoder)
        project.save()
        self.plugin_object.save(project, data)
        return project
