from django.views.generic import DetailView
from . import models
from . import utils


class ConfigurationView(DetailView):
    http_method_names = ['get']
    model = models.Project
    template_name = 'genconf/configuration.txt'

    def get_context_data(self, **kwargs):
        context = super(ConfigurationView, self).get_context_data(**kwargs)
        context['router'] = utils.router_load(kwargs['object'].configuration)
        return context
