# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, codecs


class DistributedcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingCSDNPipeline(object):
    def __init__(self):
        self.file = codecs.open('papers.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        title = json.dumps("标题：" + str(item['title']), ensure_ascii=False) + "\n"
        keyword = json.dumps("关键词：" + str(item['keyword']), ensure_ascii=False) + "\n"
        meta = json.dumps("描述：" + str(item['meta']), ensure_ascii=False) + "\n"
        content = json.dumps("内容：" + str(item['content']), ensure_ascii=False) + "\n\n"
        line = title + keyword + meta + content
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
