import os
import redis
import urlparse

REDIS_URL = urlparse.urlparse(os.environ.get('REDISCLOUD_URL', 'redis://:@localhost:6379/'))


if __name__ == "__main__":
    # Shortcut command to clear the redis.
    r = redis.StrictRedis(
        host=REDIS_URL.hostname, port=REDIS_URL.port,
        password=REDIS_URL.password)
    r.flushall()
