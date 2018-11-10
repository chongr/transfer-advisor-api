import json

from utils.redis_data.redis_client import RedisClient


class Arrivals:
    def __init__(self, route_id, gtfs_stop_id, direction, arrival_times):
        self.route_id = route_id
        self.gtfs_stop_id = gtfs_stop_id
        self.direction = direction
        # TODO: Add format validation
        # arrival_times should be of the format {"trip_id": id, "arrival_time": t, "departure_time": d}
        self.arrival_times = arrival_times

    @staticmethod
    def make_arrival_redis_key(route_id, gtfs_stop_id, direction):
        return 'ArrivalTimes/{}/{}/{}'.format(route_id, gtfs_stop_id, direction)

    def redis_key(self):
        return self.make_arrival_redis_key(self.route_id, self.gtfs_stop_id, self.direction)

    @classmethod
    def get(cls, route_id, gtfs_stop_id, direction):
        arrival_redis_key = cls.make_arrival_redis_key(route_id, gtfs_stop_id, direction)
        arrival_times = RedisClient().conn.get(arrival_redis_key)
        return cls(route_id, gtfs_stop_id, direction, json.loads(arrival_times))

    def sort_arrival_times(self):
        self.arrival_times.sort(key=lambda arrival: arrival['arrival_time'] or arrival['departure_time'])

    def save(self):
        self.sort_arrival_times()
        return RedisClient().conn.set(self.redis_key, json.dumps(self.arrival_times))

    @classmethod
    def bulk_save(cls, arrivals_to_save):
        keys_to_set = {}
        for arrival in arrivals_to_save:
            arrival.sort_arrival_times()
            keys_to_set[arrival.redis_key()] = json.dumps(arrival.arrival_times)
        return RedisClient().conn.mset(keys_to_set)


class TripArrivals:
    def __init__(self, trip_id, arrival_times):
        self.trip_id = trip_id
        # TODO: Add format validation
        # arrival_times should be of the format {"route_id": id, "gtfs_stop_id": t, "direction": d, "arrival_time": t, "departure_time": d}
        self.arrival_times = arrival_times

    @staticmethod
    def make_arrival_redis_key(trip_id):
        return 'TripArrivals/{}'.format(trip_id)

    def redis_key(self):
        return self.make_arrival_redis_key(self.trip_id)

    @classmethod
    def get(cls, trip_id):
        arrival_redis_key = cls.make_arrival_redis_key(trip_id)
        arrival_times = RedisClient().conn.get(arrival_redis_key)
        return cls(trip_id, json.loads(arrival_times))

    def sort_arrival_times(self):
        self.arrival_times.sort(key=lambda arrival: arrival['arrival_time'] or arrival['departure_time'])

    def save(self):
        self.sort_arrival_times()
        return RedisClient().conn.set(self.redis_key, json.dumps(self.arrival_times))

    @classmethod
    def bulk_save(cls, arrivals_to_save):
        keys_to_set = {}
        for arrival in arrivals_to_save:
            arrival.sort_arrival_times()
            keys_to_set[arrival.redis_key()] = json.dumps(arrival.arrival_times)
        return RedisClient().conn.mset(keys_to_set)
