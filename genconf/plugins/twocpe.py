from django import forms
from yapsy.IPlugin import IPlugin
from genconf import constants


class Wan1Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)


class TwoCpe(IPlugin):
    forms = [Wan1Form]

    def print_name(self):
        print "This is TwoCpe plugin"
