from django.contrib import admin
from . import forms
from . import models


class LoopbackInline(admin.TabularInline):
    model = models.Loopback
    form = forms.LoopbackForm
    extra = 0
    can_delete = False


@admin.register(models.Bras)
class BrasAdmin(admin.ModelAdmin):
    inlines = [LoopbackInline]


@admin.register(models.Vrf)
class VrfAdmin(admin.ModelAdmin):
    list_display = ('bras', 'number', 'name')
    list_display_links = ('number', 'name')
    search_fields = ('number', 'name')
    list_filter = ('bras',)
