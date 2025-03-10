import os
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()

redis = Redis(url=os.getenv("REDIS_URL"), token=os.getenv("REDIS_TOKEN"))


def view_count():
    redis.incr("view_count")
