# -*- coding:utf-8 -*-
import redis
import re
from urllib.parse import urlparse
# from ..settings import *

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')


# class MySpider(RedisSpider):
#     name = 'upData'
#     rds = redis.from_url(REDIS_URL, 0)
#     redis_key = 'domain:start_urls'

def parse(self, response):
    list = []
    file = open(r'E:/data/crawler/domain.csv')
    for f in file:
        word = f.decode('utf-8').strip().split(',')[0]
        if len(word) > 0 and not self.contain_zh(word):
            if not word.startswith('www'):
                word = 'www.' + word
            list.append(('http://' + word).strip())
    print(len(list))
    for i in list:
        self.rds.rpush("domain:start_urls", i)


def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    # word = word.decode()
    global zh_pattern
    match = zh_pattern.search(word)
    return match


def upload():
    list = []
    file = open('E:\\data\\crawler\\domain.csv','r',encoding = 'utf-8')
    for f in file:
        if len(f.strip().split(',')) > 0:
            word = f.strip().split(',')[0].strip()
            if len(word) > 0 and not contain_zh(word):
                if not word.startswith('www'):
                    word = 'www.' + word
                list.append(('http://' + word).strip())
    print(len(list))
    REDIS_URL = 'redis://:@localhost:18888'
    rds = redis.from_url(REDIS_URL, 0)
    for i in list:
        rds.rpush("domain:start_urls", i)


if __name__ == '__main__':
    upload()