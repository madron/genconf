from django.conf.urls import patterns, url
from django.contrib import admin
from adminwizard.admin import AdminWizard
from . import forms
from . import models
from . import views


@admin.register(models.Project)
class ProjectAdmin(AdminWizard):
    form = forms.ProjectForm
    search_fields = ['name']
    save_on_top = True
    save_as = True
    wizard_view = views.ProjectWizardView

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(?P<pk>\d+)/configuration/$',
                self.admin_site.admin_view(views.ConfigurationView.as_view()),
                name='%s_%s_configuration' % info),
        )
        return urls + super(ProjectAdmin, self).get_urls()
