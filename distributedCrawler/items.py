# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class DistributedcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PaperItem(Item):
    title = Field()  # 网页标题
    meta = Field()  # 网页meta
    keyword = Field()  # 网页关键字
    content = Field()  # 网页内容
