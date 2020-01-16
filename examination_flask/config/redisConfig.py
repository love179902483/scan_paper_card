import redis

pool = redis.ConnectionPool(host='localhost', port=6378)
redisPool = redis.Redis(connection_pool=pool)

class RedisPool():
    @staticmethod
    def redisPool():
        return redisPool

