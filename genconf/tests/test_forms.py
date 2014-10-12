from django.test import TestCase
from .. import forms


class ProjectFormTest(TestCase):
    def setUp(self):
        self.form = forms.ProjectForm
        self.data = dict(name='Test Project')

    def test_configuration_empty(self):
        form = self.form(self.data)
        self.assertEqual(form.errors, {})

    def test_configuration_ok(self):
        self.data['configuration'] = '{"_class": "router", "name": "Cisco-1801"}'
        form = self.form(self.data)
        self.assertEqual(form.errors, {})

    def test_configuration_ko(self):
        self.data['configuration'] = '{]'
        form = self.form(self.data)
        self.assertEqual(form.errors['configuration'], ['Invalid configuration.'])
