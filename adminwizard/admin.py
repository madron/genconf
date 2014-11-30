from django.db import transaction
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from . import views


class AdminWizard(admin.ModelAdmin):
    @csrf_protect_m
    @transaction.atomic
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        kwargs = dict(admin=self, object_id=object_id, form_url=form_url, extra_context=extra_context)
        return self.wizard_view.as_view()(request, **kwargs)
