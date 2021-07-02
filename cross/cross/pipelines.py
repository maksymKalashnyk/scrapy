from .items import firstLinkItem
import redis
from scutils.redis_queue import RedisQueue


class firstLinkPipeline(object):
    def __init__(self):
        self.conn = redis.Redis(host="localhost", port="6379")

    def process_item(self, item, spider):

        if isinstance(item, firstLinkItem):
            queue = RedisQueue(self.conn, "tasks")
            queue.push(item)
