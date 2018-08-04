# -*- coding: utf-8 -*-


BOT_NAME = 'distributedCrawler'

SPIDER_MODULES = ['distributedCrawler.spiders']
NEWSPIDER_MODULE = 'distributedCrawler.spiders'

ROBOTSTXT_OBEY = False


#覆盖默认请求头，可以自己编写Downloader Middlewares设置代理和UserAgent
DEFAULT_REQUEST_HEADERS = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
}
ITEM_PIPELINES = {
    # 'distributedCrawler.pipelines.JsonWithEncodingCSDNPipeline': 300,
    'distributedCrawler.pipelines.MyPipeline':300,
    'distributedCrawler.pipelines.DownloadImagesPipeline':3
}
DOWNLOADER_MIDDLEWARES = {
    # 设置不参与scrapy的自动重试的动作
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
     'distributedCrawler.middlewares.JSPageMiddleware': 543
}
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

#redis配置
REDIS_URL = None  # 一般情况可以省去
REDIS_HOST = 'localhost'  # 也可以根据情况改成 localhost
REDIS_PORT = 18888

#Mysql配置
MYSQL_HOST='localhost'
MYSQL_DBNAME='pythonspider'
MYSQL_USER='root'
MYSQL_PASSWD='actbd'
MYSQL_PORT=3306
MYSQL_CHARSET='utf8'

IMAGES_STORE='E:\\data\\picture'
DOWNLOAD_DELAY = 0.25
IMAGES_EXPIRES = 90             # 过期天数
IMAGES_MIN_HEIGHT = 100         # 图片的最小高度
IMAGES_MIN_WIDTH = 100          # 图片的最小宽度

