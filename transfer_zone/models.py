# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.db import models
from rider.models import Rider
from station.models import Station
from arrivals.models import TripArrivals
# Create your models here.


TRIP_ID_PARSER = re.compile(r'(\d{6})_(\w)..(N|S)(\w{0,3})')


class TransferZone(models.Model):
    name = models.CharField(max_length=20)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    radius = models.FloatField()
    target_station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)

    def time_to_target_station(self, transfer_station_gtfs_id, current_trip_id):
        arrivals_for_trip = TripArrivals.get(current_trip_id)
        arrival_time_at_transfer_stop = next(arrival for arrival in arrivals_for_trip.arrival_times if arrival['gtfs_stop_id'] == transfer_station_gtfs_id)
        line_to_check = self.target_station.line
        stations_in_complex_for_target_line = Station.objects.filter(complex_id=self.target_station.complex_id, subwayline=line_to_check).prefetch_related('subwayline_set')




