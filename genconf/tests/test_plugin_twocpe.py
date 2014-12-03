from django.test import TestCase
from .. import factories
from .. import models


class ProjectModelTest(TestCase):
    def test_str(self):
        project = factories.ProjectFactory(name='Test')
        self.assertEqual(str(project), 'Test')


class TwoCpePluginTest(TestCase):
    def setUp(self):
        from ..plugin import manager
        self.plugin_object = manager.getPluginByName('twocpe').plugin_object

    def test_get_objects(self):
        project = factories.ProjectFactory(name='Test')
        data = dict(
            wan1=dict(access_type='ethernet'),
            wan2=dict(access_type='adsl'),
        )
        objects = self.plugin_object.get_objects(project, data)
