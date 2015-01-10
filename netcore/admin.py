from django.contrib import admin
from . import models


@admin.register(models.Bras)
class BrasAdmin(admin.ModelAdmin):
    pass
