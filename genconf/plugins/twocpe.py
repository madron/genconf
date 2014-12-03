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

    def save_objects(self, project, objects):
        from genconf import models
        old_routers = models.Router.objects.filter(project=project).order_by('pk')
        for router in objects['routers']:
            if old_routers.count() > 0:
                try:
                    old = old_routers.get(name=router.name)
                except models.Router.DoesNotExist:
                    old = old_routers[0]
                router.pk = old.pk
            router.save()
            old_routers = old_routers.exclude(pk=router.pk)
        if old_routers.count() > 0:
            old_routers.delete()

    def get_objects(self, project, data):
        from genconf import factories
        return dict(
            routers=[
                factories.RouterFactory.build(project=project, name='wan1'),
                factories.RouterFactory.build(project=project, name='wan2'),
            ],
        )

    def save(self, project, data):
        objects = self.get_objects(project, data)
        self.save_objects(project, objects)
