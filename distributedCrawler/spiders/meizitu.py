# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider
from distributedCrawler.items import MeizituItem
from scrapy.spiders import Rule
from scrapy.http import Request


class MztSpider(RedisSpider):
    name = 'Meizitu'
    redis_key = 'image:start_urls'

    # 请求头
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
    }

    # 页面的分页
    page_lx = LinkExtractor(allow=('a/*_\d+\.html'))
    # 详细的信息
    self_lx = LinkExtractor(allow=('a/\d+\.html'))
    # 规则
    rules = (
        Rule(page_lx, follow=True),
        Rule(self_lx, callback='parse', follow=False)
    )

    # 图片分类的链接
    def parse(self, response):
        links = response.xpath('//div[@class="tags"]/span/a/@href').extract()
        for item in links:
            typeName = response.xpath('//a[re:test(@href,"' + item + '")]/text()').extract()[0]
            yield Request(url=item, headers=self.headers, callback=self.first_parse, meta={'type': typeName})

    # 每一个分类里面分页的链接
    def first_parse(self, response):
        typeName = response.meta['type']
        links = response.xpath('//a[re:test(@href,"http://www.meizitu.com/a/\d+.html")]/@href').extract()
        for item in links:
            yield Request(url=item, headers=self.headers, callback=self.second_parse, meta={'type': typeName})

    # 每一个分页里面每一页里面的链接
    def second_parse(self, response):
        item = MeizituItem()
        item['name'] = response.xpath("//h2/a/text()").extract()[0]
        item['tags'] = response.meta['type']
        item['image_urls'] = response.xpath("//div[@id='picture']/p/img/@src").extract()
        yield item
