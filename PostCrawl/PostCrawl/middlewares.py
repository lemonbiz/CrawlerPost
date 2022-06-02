# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import faker as faker
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class PostcrawlSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class PostcrawlDownloaderMiddleware:
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
        # 'http': 'http://H884Y26940NA13ND:3B8B6ACDE5871EFA@http-dyn.abuyun.com:9020',

        # request.meta['proxy'] = 'http://H884Y26940NA13ND:3B8B6ACDE5871EFA@http-dyn.abuyun.com:9020'
        return

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        #
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    # 判断请求协议头
    # 拦截的是发生异常的请求对象
    def process_exception(self, request, exception, spider):
        pass
        # # 设置代理ip
        # if request.url.split(':')[0] == 'http':
        #     request.meta['proxy'] = 'http://H884Y26940NA13ND:3B8B6ACDE5871EFA@http-dyn.abuyun.com:9020'
        # else:
        #     request.meta['proxy'] = 'http://H884Y26940NA13ND:3B8B6ACDE5871EFA@http-dyn.abuyun.com:9020'

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
