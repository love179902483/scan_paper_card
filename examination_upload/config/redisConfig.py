import redis

pool = redis.ConnectionPool(host='localhost', port=6378, db=0)
redisPool0 = redis.Redis(connection_pool=pool)

pool_1 = redis.ConnectionPool(host='localhost', port=6378, db=1)
redisPool_1 = redis.Redis(connection_pool=pool_1)

class RedisPool():
    @staticmethod
    def redisPool():
        return redisPool0
    @staticmethod
    def redisPool1():
        return redisPool_1
