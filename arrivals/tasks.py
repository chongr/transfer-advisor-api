import re
from background_task import background

from utils.management.commands.read_real_time_subway_locations import read_feed
from arrivals.models import Arrival

STATION_PARSER = re.compile(r'^(\w{3})(N|S)$')
LINES_TO_FEED_NUMBER = {
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 51,
    'N': 16,
    'W': 16
}


def parse_feed_info(entity):
    trip_update = entity.trip_update
    route_id = entity.trip_update.trip.route_id
    stop_arrival_times = []
    for stop_time_update in trip_update.stop_time_update:
        station_match = STATION_PARSER.match(stop_time_update.stop_id)
        stop_arrival_times.append(
            Arrival(route_id, station_match.group(1), station_match.group(2), stop_time_update.arrival.time)
        )
    return stop_arrival_times


@background(schedule=10)
def update_train_station_arrival_times(lines=None):
    feeds_needed = ['1', '26', '16', '21', '2', '11', '31', '36', '51']
    if lines:
        feeds_needed = []
        for line in lines:
            feeds_needed.append(LINES_TO_FEED_NUMBER[line])

    all_arrivals = []
    for feed in feeds_needed:
        feed_entities = read_feed(feed)
        for entity in feed_entities:
            all_arrivals.extend(parse_feed_info(entity))
    Arrival.bulk_save(all_arrivals)
