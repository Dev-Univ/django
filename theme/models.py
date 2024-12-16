from django.db import models


class Theme(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    description = models.TextField()
    month = models.IntegerField()
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


