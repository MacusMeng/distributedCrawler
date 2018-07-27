# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from distributedCrawler.DBHelper import MysqlHelper
import os
import requests
import scrapy
from scrapy.exceptions import DropItem
from distributedCrawler.settings import IMAGES_STORE
from scrapy.contrib.pipeline.images import ImagesPipeline

mysql = MysqlHelper()


class DistributedcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MyPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        title = item['name']
        image_guid = request.url.split('/')[-1]
        filename = 'full/{0}/{1}'.format(title, image_guid)
        return filename

    def get_media_requests(self, item, info):
        for img_url in item['imgs_url']:
            referer = item['url']
            yield scrapy.Request(img_url, meta={'item': item,'referer': referer})

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
        if spider.name == 'Meizitu':
            print("here")
        #     if 'image_urls' in item:  # 如何‘图片地址’在项目中
        #         images = []  # 定义图片空集
        #     dir_path = '%s/%s' % (IMAGES_STORE, spider.name)
        #
        #     if not os.path.exists(dir_path):
        #         os.makedirs(dir_path)
        #     for image_url in item['image_urls']:
        #         us = image_url.split('/')[3:]
        #         image_file_name = '_'.join(us)
        #         file_path = '%s/%s' % (dir_path, image_file_name)
        #         images.append(file_path)
        #         if os.path.exists(file_path):
        #             continue
        #
        #         with open(file_path, 'wb') as handle:
        #             response = requests.get(image_url, stream=True)
        #             for block in response.iter_content(1024):
        #                 if not block:
        #                     break
        #                 handle.write(block)
        #     item['images'] = images
        return item
# 图片下载方法一
class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info): #下载图片
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)}) #添加meta是为了下面重命名文件名使用

    def file_path(self,request,response=None,info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        index=request.meta['tags'] #通过上面的index传递过来列表中当前下载图片的下标

        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
        image_guid = item['name'][index]+'.'+request.url.split('/')[-1].split('.')[-1]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        filename = u'full/{0}/{1}'.format(item['tags'], image_guid)
        return filename


def spider_closed(self, spider):
    self.file.close()
