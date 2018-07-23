# coding: utf-8
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import scrapy
import re
from distributedCrawler.items import PaperItem
from urllib.parse import urlparse

class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'web_redis'
    redis_key = 'domain:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={'start_url': url})

    def parse(self, response):
        item = PaperItem()
        item['url'] = urlparse(response.url).netloc
        if response.url == 'exception':
            item['meta'] = ''
            item['keyword'] = ''
            item['title'] = ''
            item['content'] = 'unable to access'
        else:
            try:
                soup = BeautifulSoup(response.body, "lxml")
                [s.extract() for s in soup('script')]
            except:
                item['meta'] = ''
                item['keyword'] = ''
                item['title'] = ''
                item['content'] = 'unable to access'
            else:
                try:
                    content = soup.text
                    string = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', "", content)
                    item['content'] = re.sub('[\\(.*?\\)|\\{.*?}|\\[.*?]', '', string)
                except:
                    item['content'] = ''
                try:
                    item['meta'] = soup.find(attrs={"name": "description"})['content']
                except:
                    item['meta'] = ''
                try:
                    item['keyword'] = soup.find(attrs={"name": "keywords"})['content']
                except:
                    item['keyword'] = ''
                try:
                    item['title'] = re.sub('[\n\r\t]', '', soup.title.string)
                except:
                    item['title'] = ''
            return item
