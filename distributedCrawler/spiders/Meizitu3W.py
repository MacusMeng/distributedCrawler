# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from distributedCrawler.items import MeizituItem
from bs4 import BeautifulSoup
from scrapy.http import Request
import requests
import re


class Meizitu3WSpider(RedisSpider):
    name = 'Meizitu3W'
    redis_key = 'meizi:start_urls'

    # 请求头
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
    }

    def parse(self, response):
        all_a = BeautifulSoup(response.body, 'lxml').find('div', class_='all').find_all('a')
        result = []
        for a in all_a:
            if a['href'] == 'http://www.mzitu.com/old/':
                html = requests.get(a['href'])
                old_all = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
                for old in old_all:
                    result.append({'url': old['href'], 'name': old.get_text()})
            else:
                result.append({'url': a['href'], 'name': old.get_text()})
        for item in result:
            yield Request(url=item['url'], headers=self.headers, callback=self.first_parse, meta={'name': item['name']})

    def first_parse(self, response):
        href = response.url
        soup = BeautifulSoup(response.body, 'lxml')
        max_span = soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.headers['referer'] = page_url
            yield Request(url=page_url, headers=self.headers, callback=self.second_parse,
                          meta={'name': response.meta['name']})

    def second_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = MeizituItem()
        item['image_urls'] = [soup.find('div', class_='main-image').find('img')['src']]
        temp = response.meta['name']
        item['name'] = re.sub("[+——！，。？、~@#￥%……&*（）]+|[!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]".decode('utf-8'),
                              "".decode('utf-8'), temp)
        item['tags'] = '全部'.decode('utf-8')
        yield item
