# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenthopItem(scrapy.Item):
    url = scrapy.Field()
    address = scrapy.Field()
    neighborhood = scrapy.Field()
    borough = scrapy.Field()
    price = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    no_fee = scrapy.Field()
