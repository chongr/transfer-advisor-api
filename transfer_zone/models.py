# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from rider.models import Rider
# Create your models here.

class TransferZone(models.Model):
    name = models.CharField(max_length=20)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    radius = models.FloatField()
