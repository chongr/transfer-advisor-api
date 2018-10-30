from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
import requests
from requests import HTTPError

from station.models import Station
from subway_line.models import SubwayLine


MTA_STATION_URL = "http://web.mta.info/developers/data/nyct/subway/Stations.csv"
SUBWAY_LINES = ['1', '2', '3', '4', '5', '6', '7', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                'J', 'L', 'M', 'N', 'Q', 'R', 'S', 'W', 'Z']
IGNORED_LINES = ['SIR', 'SI']  # ignoring Staten Island Railway for now


class UnexpectedMTADataFormat(CommandError):
    pass


def parse_mta_station_data(data_line, subway_lines_to_stations):
    data = data_line.split(',')
    fields = Station.mta_data_fields
    if len(data) != len(fields):
        raise UnexpectedMTADataFormat("data length different than expected fields: {}".format(data))
    station = Station()
    routes = []
    for info, field in zip(data, fields):
        info = info.strip()
        if field in Station.mta_data_fields_integers:
            setattr(station, field, int(info))
        elif field in Station.mta_data_fields_location:
            setattr(station, field, float(info))
        elif field in Station.mta_data_fields_chars:
            setattr(station, field, info)
        elif field == 'daytime_routes':
            routes = info.split()

    for route in routes:
        route = route.strip()
        if route in IGNORED_LINES:
            continue
        elif route not in SUBWAY_LINES:
            raise UnexpectedMTADataFormat("{} daytime route not in expected subway routes".format(route))
        subway_lines_to_stations[route].append(station)
    return station


def match_stations_to_subway_line(subway_lines_to_stations):
    for subway_line, stations in subway_lines_to_stations.items():
        station_identifiers = [station.gtfs_stop_id for station in stations]
        all_stations = Station.objects.filter(gtfs_stop_id__in=station_identifiers)
        subway_line = SubwayLine.objects.get(pk=subway_line)
        for station in all_stations:
            subway_line.stations.add(station)
        subway_line.save()


def create_subway_lines():
    for line in SUBWAY_LINES:
        SubwayLine.objects.get_or_create(pk=line)


class Command(BaseCommand):
    help = 'load db with static files from the mta'

    def handle(self, *args, **options):
        create_subway_lines()
        resp = requests.get(MTA_STATION_URL)
        try:
            resp.raise_for_status()
        except HTTPError:
            raise CommandError("request failed to mta site with status code {}".format(resp.status_code))
        # ignore first line (headers) and last line (empty string after new line)
        all_stations_data = [data_line.strip() for data_line in resp.text.split("\r\n")[1:-1]]
        subway_lines_to_stations = defaultdict(list)
        all_stations = [parse_mta_station_data(station_data, subway_lines_to_stations) for station_data in all_stations_data]
        try:
            Station.objects.bulk_create(all_stations)
        except IntegrityError:
            print("skipping adding stations as they are already in db")

        match_stations_to_subway_line(subway_lines_to_stations)
