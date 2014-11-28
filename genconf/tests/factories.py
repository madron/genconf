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
    configuration = ''


class RouterFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Router
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    project = factory.SubFactory(ProjectFactory)
    name = 'C1801'


class VrfFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Vrf
    FACTORY_DJANGO_GET_OR_CREATE = ('router', 'name')

    router = factory.SubFactory(RouterFactory)
    name = ''


class RouteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Route

    vrf = factory.SubFactory(VrfFactory)
    name = ''


class Layer3InterfaceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Layer3Interface

    vrf = factory.SubFactory(VrfFactory)


class VlanFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Vlan
    FACTORY_DJANGO_GET_OR_CREATE = ('router', 'tag')

    router = factory.SubFactory(RouterFactory)
    tag = 1
    layer_3_interface = factory.SubFactory(Layer3InterfaceFactory)
    description = ''
    notes = ''


class PhysicalInterfaceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.PhysicalInterface
    FACTORY_DJANGO_GET_OR_CREATE = ('router', 'name')

    router = factory.SubFactory(RouterFactory)
    name = 'FA0/1'
    type = 'ethernet'
    layer = 2
    native_vlan = factory.SubFactory(VlanFactory)


class SubInterfaceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.SubInterface
    FACTORY_DJANGO_GET_OR_CREATE = ('physical_interface', 'name')

    physical_interface = factory.SubFactory(PhysicalInterfaceFactory)
    name = 'Fa0.5'
    type = 'ethernet'
    layer = 2
    vlan = factory.SubFactory(VlanFactory)
