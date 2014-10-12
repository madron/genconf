from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    json = models.TextField(blank=True)

    def __str__(self):
        return self.name
