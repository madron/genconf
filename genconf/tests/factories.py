import factory
from django.contrib.auth.models import User
from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = 'test'
    is_active = True
    is_superuser = True
    is_staff = True
    # 'pass'
    password = 'pbkdf2_sha256$12000$LWhlUQyAntYP$FtxgZ9CnZBTbrvcjHJO6StuAJoQqMRDRTFXzYtxRRhg='
    email = 'test@example.com'


class ProjectFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Project
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = 'Project name'
    configuration = '{"_class": "router", "name": "Cisco-1801"}'
