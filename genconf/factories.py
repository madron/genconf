import factory
from . import models


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project
        django_get_or_create = ('name',)

    name = ''
    configuration = ''


class RouterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Router
        django_get_or_create = ('name',)

    project = factory.SubFactory(ProjectFactory)
    name = ''


class VrfFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vrf
        django_get_or_create = ('router', 'name',)

    router = factory.SubFactory(RouterFactory)
    name = ''


class RouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Route

    vrf = factory.SubFactory(VrfFactory)
    name = ''


class VlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vlan
        django_get_or_create = ('router', 'tag',)

    router = factory.SubFactory(RouterFactory)
    tag = 1
    description = ''


class PhysicalInterfaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PhysicalInterface
        django_get_or_create = ('router', 'name',)

    router = factory.SubFactory(RouterFactory)
    name = ''
    type = 'ethernet'
    layer = 2
    native_vlan = factory.SubFactory(VlanFactory)


class SubInterfaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SubInterface
        django_get_or_create = ('physical_interface', 'name',)

    physical_interface = factory.SubFactory(PhysicalInterfaceFactory)
    name = ''
    layer = 2
    vlan = factory.SubFactory(VlanFactory)


class Layer3InterfaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Layer3Interface

    vrf = factory.SubFactory(VrfFactory)


class PhysicalLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PhysicalLink

    project = factory.SubFactory(ProjectFactory)
    router_interface_1 = factory.SubFactory(PhysicalInterfaceFactory)
    router_interface_2 = factory.SubFactory(PhysicalInterfaceFactory)
