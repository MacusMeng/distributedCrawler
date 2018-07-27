# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider
from  distributedCrawler.items import MeizituItem
from scrapy.spiders import  Rule
import scrapy
import os
class MztSpider(RedisSpider):
    name = 'Meizitu'
    redis_key = 'image:start_urls'

    #请求头
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'www.meizitu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
    }

    #中国红娘index页面的分页
    page_lx = LinkExtractor(allow=('a/more_\d+'))
    #个人详细的信息
    self_lx = LinkExtractor(allow=('a/\d+'))
    #规则
    rules = (
        Rule(page_lx,follow=True),
        Rule(self_lx,callback='parse',follow=False)
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MztSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        #获取图片集连接
        links=response.xpath('//a[re:test(@href,"http://www.meizitu.com/a/\d+.html")]/@href').extract()
        print (links)
        #对所有的图片集进行请求
        for url in links:
            yield scrapy.Request(url=url,headers=self.headers,callback=self.parseImageArticle)

    def parse_item(self, response):
        item = MeizituItem()
        item['name'] = response.xpath("//h2/a/text()").extract()
        item['tags'] = response.xpath(
            "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p").extract()
        item['image_urls'] = response.xpath("//div[@id='picture']/p/a/img/@src").extract()
        return item

    #解析单个图片集的响应
    def parseImageArticle(self,response):
        #获取图片链接列表
        src_links=response.xpath('//img[re:test(@src,"http://mm.howkuai.com/wp-content/uploads/20\d{2}a/\d{2}/\d{2}/\d+.jpg")]/@src').extract()
        #获取图片集名称，用以创建文件夹
        base_path=os.path.join("image",response.xpath('//div[contains(@class,"metaRight")]/h2/a/text()').extract()[0])
        #下载图片请求头
        header={
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
        }
        #文件夹不存在则创建
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        #下载图片
        for i in range(len(src_links)):
            #获取用以存储的文件名
            file_path = os.path.join(base_path, str(i)+'.jpg')
            #传递文件名，并使用imageDownload方法解析
            yield scrapy.Request(src_links[i],meta={'file_path':file_path},headers=header,callback=self.imageDownload)
        #获取当前页面的其他图片集链接
        links = response.xpath('//a[re:test(@href,"http://www.meizitu.com/a/\d+.html")]/@href').extract()
        print (links)
        #请求其他图片集，使用此方法解析
        for url in links:
            yield scrapy.Request(url, headers=self.headers, callback=self.parseImageArticle)
