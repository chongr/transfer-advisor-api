import re
from collections import defaultdict
from background_task import background

from utils.management.commands.read_real_time_subway_locations import read_feed
from arrivals.models import Arrivals, TripArrivals


STATION_PARSER = re.compile(r'^(\w{3})(N|S)$')
LINES_TO_FEED_NUMBER = {
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 51,
    'N': 16,
    'W': 16
}


def parse_feed_info(entity, current_arrivals):
    """
    takes a single entity in the mta feed and adds to the current_arrivals dict
    returns all trip arrivals for this one trip_id
    :returns : the trip id which this entity pertains to and all_arrivals associated with it
    """
    trip_update = entity.trip_update
    route_id = entity.trip_update.trip.route_id
    trip_id = entity.trip_update.trip.trip_id
    trip_arrival_times = []
    for stop_time_update in trip_update.stop_time_update:
        station_match = STATION_PARSER.match(stop_time_update.stop_id)
        gtfs_stop_id = station_match.group(1)
        direction = station_match.group(2)
        arrival_time = stop_time_update.arrival.time
        departure_time = stop_time_update.departure.time
        arrival_key = Arrivals.make_arrival_redis_key(route_id, gtfs_stop_id, direction)
        current_arrivals[arrival_key].append({"trip_id": trip_id, "arrival_time": arrival_time, "departure_time": departure_time})
        trip_arrival_times.append({"route_id": route_id, "gtfs_stop_id": gtfs_stop_id, "direction": direction, "arrival_time": arrival_time, "departure_time": departure_time})
    return trip_id, trip_arrival_times

# @background(schedule=10)
def update_train_station_arrival_times(lines=None):
    feeds_needed = ['1', '26', '16', '21', '2', '11', '31', '36', '51']
    if lines:
        feeds_needed = []
        for line in lines:
            feeds_needed.append(LINES_TO_FEED_NUMBER[line])

    current_arrivals = defaultdict(list)
    all_trip_arrivals = []
    for feed in feeds_needed:
        feed_entities = read_feed(feed)
        for entity in feed_entities:
            trip_id, trip_arrival_times = parse_feed_info(entity, current_arrivals)
            all_trip_arrivals.append(TripArrivals(trip_id, trip_arrival_times))
    TripArrivals.bulk_save(all_trip_arrivals)

    all_arrivals = []
    for arrival_redis_key, arrival_times in current_arrivals.items():
        _, route_id, gtfs_stop_id, direction = arrival_redis_key.split('/')
        all_arrivals.append(Arrivals(route_id, gtfs_stop_id, direction, arrival_times))
    Arrivals.bulk_save(all_arrivals)
