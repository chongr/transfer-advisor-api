# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from rider.models import Rider
from station.models import Station
# Create your models here.

class TransferZone(models.Model):
    name = models.CharField(max_length=20)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    radius = models.FloatField()
    target_station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)
