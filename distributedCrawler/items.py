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


# 域名爬取
class PaperItem(Item):
    url = Field()  # url
    title = Field()  # 网页标题
    meta = Field()  # 网页meta
    keyword = Field()  # 网页关键字
    content = Field()  # 网页内容


# 红娘网站信息爬取
class HongniangItem(Item):
    """
    中国红娘网站  女用户   简单字段
    """
    # 用户名称
    nickname = Field()
    # 用户id
    loveid = Field()
    # 用户的照片
    photos = Field()
    # 用户年龄
    age = Field()
    # 用户的身高
    height = Field()
    # 用户是否已婚
    ismarried = Field()
    # 用户年收入
    yearincome = Field()
    # 用户的学历
    education = Field()
    # 用户的地址
    workaddress = Field()
    # 用户的内心独白
    soliloquy = Field()
    # 用户的性别
    gender = Field()

class MeizituItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()