from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    save_on_top = True
    save_as = True
