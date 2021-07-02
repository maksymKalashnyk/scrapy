import sys
from unittest import runner
import redis
import scrapy
from scrapy import item
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils import url
from scutils.redis_queue import RedisQueue
from twisted.internet import defer, reactor
from ..items import firstLinkItem
from scrapy.loader import ItemLoader
import redis
from scutils.redis_queue import RedisQueue


class StartLinkSpider(scrapy.Spider):
    name = "startLink"
    start_urls = ["https://www.kreuzwort-raetsel.net/uebersicht.html"]

    def __init__(self):
        self.con = redis.Redis(host="localhost", port="6379")
        self.queue = RedisQueue(self.con, "tasks")

    def parse(self, response):
        for letter in response.css("ul.dnrg li"):
            # item = ItemLoader(item=firstLinkItem(), selector=letter)

            # item.add_css("link", "a::attr(href)")
            # item.add_value("next", "SecondLinkSpider")

            # yield item.load_item()
            item = {
                "link": "https://www.kreuzwort-raetsel.net/"
                + letter.css("a").attrib["href"],
                "next": "SecondLinkSpider",
            }

            yield self.queue.push(item)


class SecondLinkSpider(scrapy.Spider):
    name = "secondLink"
    start_urls = []

    def __init__(self, url):
        self.start_urls = [url]
        self.con = redis.Redis(host="localhost", port="6379")
        self.queue = RedisQueue(self.con, "tasks")

    def parse(self, response):
        print(100 * "-")
        for paginate in response.css("ul.dnrg li"):
            # yield {"link": paginate.css("a").get()}
            item = {
                "link": "https://www.kreuzwort-raetsel.net/"
                + paginate.css("a").attrib["href"],
                "next": "TEST_SUKA",
            }

            yield self.queue.push(item)


conn = redis.Redis(host="localhost", port="6379")
queue = RedisQueue(conn, "tasks")
switcher = {"SecondLinkSpider": lambda _: SecondLinkSpider(_)}

process = CrawlerProcess()
process.crawl(StartLinkSpider)
process.start()
process.join()


loop = True

while loop:
    print("-" * 100)

    task = queue.pop()
    print(task)
    print("-" * 100)

    if task is None:
        sys.exit(0)

    # print(task)

    newClass = switcher[task["next"]](task["link"])

    # runner = CrawlerRunner()
    process.crawl(newClass.__class__, url=task["link"])
    process.start()
    process.join()
    # d = runner.crawl(newClass.__class__, url=task["link"])
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()

    print("-" * 100)
    sys.exit(0)
