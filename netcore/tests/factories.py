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


class BrasFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Bras

    name = ''


class VrfFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Vrf

    bras = factory.SubFactory(BrasFactory)
    name = ''


class LoopbackFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Loopback

    bras = factory.SubFactory(BrasFactory)
    ip = '127.0.0.1'
    vrf = factory.SubFactory(VrfFactory)
