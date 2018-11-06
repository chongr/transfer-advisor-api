from utils.redis_data.redis_client import RedisClient

class Arrival:
    def __init__(self, route_id, gtfs_stop_id, direction, arrival_time):
        self.route_id = route_id
        self.gtfs_stop_id = gtfs_stop_id
        self.direction = direction
        self.arrival_time = arrival_time

    @staticmethod
    def make_arrival_redis_key(route_id, gtfs_stop_id, direction):
        return 'ArrivalTimes/{}/{}/{}'.format(route_id, gtfs_stop_id, direction)

    def redis_key(self):
        return self.make_arrival_redis_key(self.route_id, self.gtfs_stop_id, self.direction)

    @classmethod
    def get(cls, route_id, gtfs_stop_id, direction):
        arrival_redis_key = cls.make_arrival_redis_key(route_id, gtfs_stop_id, direction)
        arrival_time = RedisClient().conn.get(arrival_redis_key)
        return cls(route_id, gtfs_stop_id, direction, arrival_time)

    def save(self):
        return RedisClient().conn.set(self.redis_key, self.arrival_time)

    @classmethod
    def bulk_save(cls, arrivals_to_save):
        keys_to_set = {}
        for arrival in arrivals_to_save:
            keys_to_set[arrival.redis_key()] = arrival.arrival_time
        return RedisClient().conn.mset(keys_to_set)
