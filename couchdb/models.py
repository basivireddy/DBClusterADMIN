from __future__ import unicode_literals

from django.db import models
class CouchCluster(models.Model):
    name = models.CharField(max_length=250)
    numofnodes = models.CharField(max_length=500)
    ips = models.CharField(max_length=100)
    names = models.CharField(max_length=100,default="")
    haport = models.IntegerField(default=0)

    def __str__(self):
        return self.name
# Create your models here.
