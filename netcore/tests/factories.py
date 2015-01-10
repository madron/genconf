import factory
from django.contrib.auth.models import User
from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'test'
    is_active = True
    is_superuser = True
    is_staff = True
    # 'pass'
    password = 'pbkdf2_sha256$12000$LWhlUQyAntYP$FtxgZ9CnZBTbrvcjHJO6StuAJoQqMRDRTFXzYtxRRhg='
    email = 'test@example.com'


class BrasFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Bras

    name = ''


class VrfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vrf

    bras = factory.SubFactory(BrasFactory)
    name = ''


class LoopbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Loopback

    bras = factory.SubFactory(BrasFactory)
    ip = '127.0.0.1'
    vrf = factory.SubFactory(VrfFactory)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    bras = factory.SubFactory(BrasFactory)
    ipnetwork = '10.0.0.0/30'
    description = ''
    vrf = factory.SubFactory(VrfFactory)
