from __future__ import unicode_literals

from django.db import models


class MongodbCluster(models.Model):
    cname = models.CharField(max_length=250)
    numofnodes = models.CharField(max_length=500)
    ips = models.CharField(max_length=100)
    names = models.CharField(max_length=100)

    def __str__(self):
        return self.cname + "-" + self.names