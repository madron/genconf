from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Project, ProjectAdmin)
