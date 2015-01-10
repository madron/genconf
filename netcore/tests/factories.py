import factory
from .. import models


class BrasFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Bras

    name = ''
