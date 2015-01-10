from django.db import models
from netutils.modelfields import NetIPAddressField


class Bras(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    management_ip = NetIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name
