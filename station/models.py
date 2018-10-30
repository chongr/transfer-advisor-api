# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Station(models.Model):
    mta_data_fields = ['id', 'complex_id', 'gtfs_stop_id', 'division',
                       'line', 'stop_name', 'borough', 'daytime_routes',
                       'structure', 'gtfs_lat', 'gtfs_lon']
    mta_data_fields_integers = ['id', 'complex_id']
    mta_data_fields_chars = ['gtfs_stop_id', 'division', 'line', 'stop_name', 'borough']
    mta_data_fields_location = ['gtfs_lat', 'gtfs_lon']

    id = models.IntegerField()
    complex_id = models.IntegerField()
    gtfs_stop_id = models.CharField(max_length=3, primary_key=True)
    division = models.CharField(max_length=3)
    line = models.CharField(max_length=128)
    stop_name = models.CharField(max_length=128)
    borough = models.CharField(max_length=3)
    # daytime_routes = models.ManyToManyField(Line)
    structure = models.CharField(max_length=128)
    gtfs_lat = models.DecimalField(max_digits=12, decimal_places=9)
    gtfs_lon = models.DecimalField(max_digits=12, decimal_places=9)
