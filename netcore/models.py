from django.db import models
from netutils.modelfields import NetIPAddressField, NetIPNetworkField


class Bras(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    management_ip = NetIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'bras'
        ordering = ['name']

    def __str__(self):
        return self.name


class Vrf(models.Model):
    bras = models.ForeignKey(Bras, db_index=True)
    number = models.IntegerField(db_index=True)
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        verbose_name_plural = 'vrf'
        ordering = ['bras__name', 'number', 'name']
        unique_together = [
            ['bras', 'number'],
            ['bras', 'name'],
        ]
        index_together = [
            ['bras', 'number', 'name'],
            ['bras', 'name'],
        ]

    def __str__(self):
        return '%d %s (%s)' % (self.number, self.name, self.bras)


class Loopback(models.Model):
    bras = models.ForeignKey(Bras, db_index=True)
    number = models.IntegerField()
    ip = NetIPAddressField()
    vrf = models.ForeignKey(Vrf, blank=True, null=True)

    class Meta:
        ordering = ['bras__name', 'number']
        unique_together = [
            ['bras', 'number'],
        ]
        index_together = [
            ['bras', 'number'],
        ]

    def __str__(self):
        return 'Loopback%d' % self.number


class Section(models.Model):
    bras = models.ForeignKey(Bras, db_index=True)
    ipnetwork = NetIPNetworkField(db_index=True)
    description = models.CharField(max_length=200, blank=True)
    vrf = models.ForeignKey(Vrf, blank=True, null=True)

    class Meta:
        ordering = ['bras__name', 'ipnetwork']
        unique_together = [
            ['bras', 'ipnetwork'],
        ]
        index_together = [
            ['bras', 'ipnetwork'],
        ]

    def __str__(self):
        return str(self.ipnetwork)
