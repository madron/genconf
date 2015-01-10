from django.contrib import admin
from . import models


@admin.register(models.Bras)
class BrasAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Vrf)
class VrfAdmin(admin.ModelAdmin):
    list_display = ('bras', 'number', 'name')
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name')
    list_filter = ('bras',)
