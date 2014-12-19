from django.views.generic import DetailView
from . import models


class ConfigurationView(DetailView):
    http_method_names = ['get']
    model = models.Router
    template_name = 'genconf/configuration/configuration.txt'
