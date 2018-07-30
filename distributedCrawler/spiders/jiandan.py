# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from distributedCrawler.items import MeizituItem
from bs4 import BeautifulSoup


class JianDanSpider(RedisSpider):
    name = 'jiandan'
    redis_key = 'jiandan:start_urls'

    # 请求头
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
    }

    # 页面的分页
    page_lx = LinkExtractor(allow=('page-\d+\#comments'))
    # 详细的信息
    self_lx = LinkExtractor(allow=('page-\d+\#comments'))
    # 规则
    rules = (
        Rule(page_lx, follow=True),
        Rule(self_lx, callback='parse', follow=False)
    )

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html.parser")
        item = MeizituItem()
        item['tags'] = '煎蛋'
        item['name'] = '美女'
        item['image_urls'] = []
        # sites = soup.findAll("a", {'class': 'view_img_link'})
        # # urls =response.xpath('//div[@class="text"]/p/img/@src').extract()
        # for site in sites:
        #     image_url = site.get('href')
        #     if not image_url.startswith('http'):
        #         image_url = 'http:' + image_url
        #     item['image_urls'].append(image_url)
        #     soup = BeautifulSoup(data, "html.parser")  # 解析网页
        images = soup.select("a.view_img_link")  # 定位元素
        for i in images:
            z = i.get('href')
            if str('gif') in str(z):
                pass
            else:
                http_url = "http:" + z
                item['image_urls'].append(http_url)
                print(http_url)
        yield item
