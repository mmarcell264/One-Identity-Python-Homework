from django.db import models

# Create your models here.


class KeyValue(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=2500)