# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from distributedCrawler.DBHelper import MysqlHelper
import os
import requests
from scrapy.http import Request
from distributedCrawler.settings import IMAGES_STORE
from scrapy.contrib.pipeline.images import ImagesPipeline

mysql = MysqlHelper()


class DistributedcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MyPipeline(ImagesPipeline):
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
        if spider.name == 'jiandan':
            if 'image_urls' in item:  # 如何‘图片地址’在项目中
                images = []  # 定义图片空集
            dir_path = '%s/%s' % (IMAGES_STORE, spider.name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                us = image_url.split('/')[3:]
                image_file_name = '_'.join(us)
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue

                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            item['images'] = images
        return item


# 图片下载方法一
class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  # 下载图片
        for image_url in item['image_urls']:
            yield Request(image_url,meta={'item': item, 'index': item['image_urls'].index(image_url)})  # 添加meta是为了下面重命名文件名使用

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = item['tags']  # 图片分类
        filename=''
        # 图片文件名
        names = request.url.split('/')
        image_guid = names[len(names) - 1]
        if not image_guid.endswith('gif'):
            filename = u'full/{0}/{1}/{2}'.format(index, item['name'], image_guid)
        return filename


def spider_closed(self, spider):
    self.file.close()
