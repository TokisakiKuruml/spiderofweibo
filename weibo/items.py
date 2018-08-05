# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection=table = 'weibo'
    id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    fans_count = scrapy.Field()
    follows_count = scrapy.Field()
    weibos_count = scrapy.Field()
    verified = scrapy.Field()
    verified_reason = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()

class UserRelationItem(scrapy.Item):
    collection = table = 'weibo'
    id = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()

