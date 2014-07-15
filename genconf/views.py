from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.loader import get_template
from django.views.generic import FormView
from . import forms
from . import utils


class GenConfView(FormView):
    form_class = forms.GenConfForm
    template_name = 'genconf/home.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        config = utils.get_config(form.cleaned_data)
        cisco = utils.get_cisco_config(config, 0)
        print cisco
        return super(GenConfView, self).form_valid(form)