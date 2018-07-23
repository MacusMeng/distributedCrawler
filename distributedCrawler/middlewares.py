# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.http import HtmlResponse


class DistributedcrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DistributedcrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # content = self.selenium_request(request.url)
        # if content.strip() != '':
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        return None
        # # return None
        # return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)


def process_response(self, request, response, spider):
    # Called with the response returned from the downloader.

    # Must either;
    # - return a Response object
    # - return a Request object
    # - or raise IgnoreRequest
    return response


def process_exception(self, request, exception, spider):
    # Called when a download handler or a process_request()
    # (from other downloader middleware) raises an exception.

    # Must either:
    # - return None: continue processing this exception
    # - return a Response object: stops process_exception() chain
    # - return a Request object: stops process_exception() chain
    if isinstance(exception, self.ALL_EXCEPTIONS):
        # 在日志中打印异常类型
        print('Got exception: %s' % (exception))
        # 随意封装一个response，返回给spider
        response = HtmlResponse(url='exception')
        return response
        # 打印出未捕获到的异常
    print('not contained exception: %s' % exception)


def spider_opened(self, spider):
    spider.logger.info('Spider opened: %s' % spider.name)


# from selenium import webdriver
# from scrapy.http import HtmlResponse
#
#
# class JSPageMiddleware(object):
#     def process_request(self, request, spider):
#         if spider.name == 'web_redis':
#             chrome_options = webdriver.ChromeOptions()
#             # 使用headless无界面浏览器模式
#             chrome_options.add_argument('--headless')
#             chrome_options.add_argument('--disable-gpu')
#             brower = webdriver.Chrome('F:\\software\\chrome\\chromedriver.exe',0,chrome_options)
#             brower.get(request.url)
#             print('访问:{0}'.format(request.url))
#             return HtmlResponse(url=brower.current_url, body=brower.page_source, encoding='utf-8', request=request)
