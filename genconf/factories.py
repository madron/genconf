import factory
from . import models


class ProjectFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Project
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = ''
    type = 'twocpe'
    configuration = ''


class RouterFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Router
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    project = factory.SubFactory(ProjectFactory)
    name = ''


class VrfFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Vrf
    FACTORY_DJANGO_GET_OR_CREATE = ('router', 'name')

    router = factory.SubFactory(RouterFactory)
    name = ''


class RouteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Route

    vrf = factory.SubFactory(VrfFactory)
    name = ''


class VlanFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Vlan
    FACTORY_DJANGO_GET_OR_CREATE = ('router', 'tag')

    router = factory.SubFactory(RouterFactory)
    tag = 1
    description = ''
    notes = ''


class PhysicalInterfaceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.PhysicalInterface
    FACTORY_DJANGO_GET_OR_CREATE = ('router', 'name')

    router = factory.SubFactory(RouterFactory)
    name = ''
    type = 'ethernet'
    layer = 2
    native_vlan = factory.SubFactory(VlanFactory)


class SubInterfaceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.SubInterface
    FACTORY_DJANGO_GET_OR_CREATE = ('physical_interface', 'name')

    physical_interface = factory.SubFactory(PhysicalInterfaceFactory)
    name = ''
    type = 'ethernet'
    layer = 2
    vlan = factory.SubFactory(VlanFactory)


class Layer3InterfaceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Layer3Interface

    vrf = factory.SubFactory(VrfFactory)
    vlan = factory.SubFactory(VlanFactory)
    subinterface = factory.SubFactory(SubInterfaceFactory)


class PhysicalLinkFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.PhysicalLink

    project = factory.SubFactory(ProjectFactory)
    endpoint_1 = factory.SubFactory(PhysicalInterfaceFactory)
    endpoint_2 = factory.SubFactory(PhysicalInterfaceFactory)
