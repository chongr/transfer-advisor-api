import urllib.request

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from google.transit import gtfs_realtime_pb2


MTA_FEED_URL = 'http://datamine.mta.info/mta_esi.php?key={key}&feed_id={id}'


class Command(BaseCommand):
    help = 'read the real time feed from the mta'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', type=str)

    def handle(self, *args, **options):
        feed_id = options['poll_id']
        feed = gtfs_realtime_pb2.FeedMessage()
        resp = urllib.request.urlopen(MTA_FEED_URL.format(key=settings.MTA_API_KEY, id=feed_id))
        print(feed.ParseFromString(resp.read()))
        print(feed.entity)


