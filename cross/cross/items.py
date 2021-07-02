import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def add_domain(value):
    return "https://www.kreuzwort-raetsel.net/" + value


class firstLinkItem(scrapy.Item):
    link = scrapy.Field(
        input_processor=MapCompose(remove_tags, add_domain),
        output_processor=TakeFirst(),
    )
    next = scrapy.Field(output_processor=TakeFirst())
