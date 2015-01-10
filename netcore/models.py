from django.db import models
from netutils.modelfields import NetIPAddressField


class Bras(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    management_ip = NetIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'bras'

    def __str__(self):
        return self.name


class Vrf(models.Model):
    bras = models.ForeignKey(Bras)
    number = models.IntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=200, db_index=True, unique=True)

    class Meta:
        verbose_name_plural = 'vrf'

    def __str__(self):
        return '%d %s (%s)' % (self.number, self.name, self.bras)
