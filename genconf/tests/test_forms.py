from django.test import TestCase
from .. import forms


class ProjectFormTest(TestCase):
    def setUp(self):
        self.form = forms.ProjectForm
        self.data = dict(name='Test Project', type='twocpe')

    def test_configuration_empty(self):
        form = self.form(self.data)
        self.assertEqual(form.errors, {})
