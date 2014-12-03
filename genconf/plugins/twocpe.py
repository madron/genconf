from django import forms
from yapsy.IPlugin import IPlugin
from genconf import constants


class Wan1Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)


class Wan2Form(forms.Form):
    access_type = forms.ChoiceField(choices=constants.ACCESS_TYPE_CHOICES)


class TwoCpe(IPlugin):
    form_list = [
        ('wan1', Wan1Form),
        ('wan2', Wan2Form),
    ]

    def get_objects(self, project, data):
        pass

    def save(self, project, data):
        pass
