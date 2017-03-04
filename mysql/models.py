from __future__ import unicode_literals

from django.db import models

class MysqlCluster(models.Model):
    name = models.CharField(max_length=250)
    numofnodes = models.CharField(max_length=500)
    ips = models.CharField(max_length=100)
    names = models.CharField(max_length=100,default="")
    slaveips = models.CharField(max_length=100,default="")
    slavenames = models.CharField(max_length=100,default="")
    numofsalvenodes = models.IntegerField(default=0)
    haport = models.IntegerField(default=0)

    def __str__(self):
        return self.name

