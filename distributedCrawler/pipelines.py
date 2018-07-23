# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from distributedCrawler.DBHelper import MysqlHelper

mysql = MysqlHelper()


class DistributedcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'web_redis':
            sql = 'insert into web(url,title,keyword,meta,content)  values(%s,%s,%s,%s,%s)'
            params = [str(item['url']), str(item['title']), str(item['keyword']), str(item['meta']),
                      str(item['content'])]
            mysql.insert(sql=sql, params=params)
        if spider.name == 'hongniangSpider':
            # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
            photos = ','.join(item['photos'])
            sql = 'insert into hongniang(nickname,loveid,photos,age,height,ismarried,yearincome,education,workaddress,soliloquy,gender)  ' \
                  'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)';
            params = [str(item['nickname']), str(item['loveid']), str(photos), str(item['age'])
                , str(item['height']), str(item['ismarried']), str(item['yearincome']), str(item['education'])
                , str(item['workaddress']), str(item['soliloquy']), str(item['gender'])]
            mysql.insert(sql=sql, params=params)
        return item


def spider_closed(self, spider):
    self.file.close()
