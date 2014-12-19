import json
from collections import OrderedDict
from django.contrib.formtools.wizard.views import SessionWizardView
from adminwizard.views import AdminWizardView
from . import models
from . import serializers
from .forms import ProjectFormStart


class BaseProjectWizardView(AdminWizardView, SessionWizardView):
    wizard_name = ''
    form_list = [
        ('start', ProjectFormStart),
    ]

    def get_form_initial(self, step):
        if step == 'start':
            return super(BaseProjectWizardView, self).get_form_initial(step)
        return self.initial_dict.get(step, {})

    def dispatch(self, request, *args, **kwargs):
        if not self.initial_dict:
            object_id = kwargs.get('object_id')
            if object_id:
                project = models.Project.objects.get(pk=object_id)
                if project.configuration:
                    self.initial_dict = json.loads(project.configuration)
        return super(BaseProjectWizardView, self).dispatch(request, *args, **kwargs)

    def save(self, form):
        data = OrderedDict()
        for step in self.form_list.keys():
            if not step == 'start':
                data[step] = self.get_cleaned_data_for_step(step)
        project = form.save(commit=False)
        project.configuration = json.dumps(data, indent=4, cls=serializers.ProjectEncoder)
        project.wizard = self.wizard_name
        project.save()
        self.save_project(project, data)
        return project

    def save_project(self, project_instance, data):
        raise NotImplementedError()
