from django.conf.urls import patterns, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import forms
from . import models
from . import views


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    form = forms.ProjectForm
    search_fields = ['name']
    save_on_top = True
    save_as = True
    change_form_template = 'genconf/project/change_form.html'

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(?P<pk>\d+)/configuration/$',
                self.admin_site.admin_view(views.ConfigurationView.as_view()),
                name='%s_%s_configuration' % info),
        )
        return urls + super(ProjectAdmin, self).get_urls()
