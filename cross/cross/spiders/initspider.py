import sys

from twisted.internet import defer, reactor
from .secondlinkspider import SecondLinkSpider
import redis
import scrapy
from scrapy.crawler import CrawlerRunner
from scutils.redis_queue import RedisQueue
from .startlinkspider import StartLinkSpider


class InitSpider(scrapy.Spider):
    name = "init"


conn = redis.Redis(host="localhost", port="6379")
queue = RedisQueue(conn, "tasks")
switcher = {"SecondLinkSpider": lambda link: SecondLinkSpider(link)}
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(StartLinkSpider)
    reactor.stop()


crawl()
reactor.run()

loop = True

while loop:
    task = queue.pop()
    print(task)
    if task is None:
        sys.exit()
