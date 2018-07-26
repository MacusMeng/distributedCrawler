from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import  Rule
class AnjuSpider(RedisCrawlSpider):
    name = "anjuke"
    redis_key = 'anju:start_urls'
    #index页面的分页
    page_lx = LinkExtractor(allow=('/p\d+'))
    #详细的信息
    self_lx = LinkExtractor(allow=('\d+'))
    #规则
    rules = (
        Rule(page_lx,follow=True),
        Rule(self_lx,callback='parse_item',follow=False)
    )

    def parse_item(self, response):
        price = self.get_age(response)
        print(price)


    def get_age(self, response):
        age = response.xpath('//span[@class="price"]/em/text()').extract()
        if len(age) > 0:
            age = age.strip()
        else:
            age = "NULL"
        return age

