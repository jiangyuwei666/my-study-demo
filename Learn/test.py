from redis import StrictRedis, ConnectionPool

url = 'redis://@localhost:6379/1'
pool = ConnectionPool.from_url(url)
redis = StrictRedis(connection_pool=pool)
print(redis.randomkey())


