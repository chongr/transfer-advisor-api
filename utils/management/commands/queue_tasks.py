from django.core.management.base import BaseCommand
from django.conf import settings

from arrivals.tasks import update_train_station_arrival_times

class Command(BaseCommand):
    help = 'setup queue tasks to update subway arrival data'

    def handle(self, *args, **options):
        update_train_station_arrival_times(['6', 'N', 'W', '7'], repeat=10)
