import scrapy


class SecondLinkSpider(scrapy.Spider):
    name = "secondLink"
    start_urls = []

    def __init__(self, url):
        # print(url)
        self.start_urls = [url]

    def parse(self, response):
        print(10 * '-')
        for paginate in response.css("ul.dnrg li"):
            yield {"link": paginate.css("a").get()}
