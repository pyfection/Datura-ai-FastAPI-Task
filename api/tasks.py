import redis
from api.celery_config import app

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.task(name="tasks.delete_redis_key")
def delete_redis_key(key):
    redis_client.delete(key)
