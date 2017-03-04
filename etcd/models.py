from __future__ import unicode_literals

from django.db import models

class EtcdCluster(models.Model):
    name = models.CharField(max_length=250)
    cname = models.CharField(max_length=100,default="")
    numofnodes = models.IntegerField()
    nodesname = models.CharField(max_length=100,default="")
    ips = models.CharField(max_length=100)
    peerport = models.CharField(max_length=100,default="")
    clientport = models.CharField(max_length=100,default="")
    isdeployed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

