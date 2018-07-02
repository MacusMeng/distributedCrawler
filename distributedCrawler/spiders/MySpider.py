# coding: utf-8
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import re
import sys
from distributedCrawler.items import PaperItem

reload(sys)
sys.setdefaultencoding("utf-8")


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'domain:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = PaperItem()
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
                string = re.sub("[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\'\:\-\;\>\<]+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"),
                                "".decode("utf8"),
                                content)
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
