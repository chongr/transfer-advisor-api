# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from station.models import Station


# Create your models here.
class SubwayLine(models.Model):
    name = models.CharField(max_length=1, primary_key=True)
    stations = models.ManyToManyField(Station)
