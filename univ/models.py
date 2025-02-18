from django.db import models

from univ.choices import Region


class Univ(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    region = models.CharField(max_length=100, choices=Region.choices)

    def __str__(self):
        return self.name
