"""
滁州市人民政府


"""
import copy

import scrapy
import scrapy_splash
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from PostCrawl.utils.data_get import HandleRequest, GetData


class ChuzhougovproSpider(CrawlSpider):
    name = 'ChuZhouGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://www.chuzhou.gov.cn/public/column/152523227?type=4&catId=151969574&action=list',
                  'https://www.chuzhou.gov.cn/public/column/152523227?type=4&action=list&nav=3&sub=&catId=151969595',]

    def start_requests(self):
        # url_list_1 = [
        #     "https://www.chuzhou.gov.cn/chuzhou/site/label/8888?IsAjax=1&dataType=html&_=0.3740558893191772&labelName=publicInfoList&siteId=2653861&pageSize=20&pageIndex={}&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=152523227&type=4&catId=151969574&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&title=&fileNum=&keyWords=&file=%2Fc1%2Fchuzhou%2FpublicInfoList_newest".format(
        #         i + 1) for i in range(327)]
        # url_list_2 = [
        #     "https://www.chuzhou.gov.cn/chuzhou/site/label/8888?IsAjax=1&dataType=html&_=0.7388437215457755&labelName=publicInfoList&siteId=2653861&pageSize=20&pageIndex={}&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=152523227&type=4&catId=151969595&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&title=&fileNum=&keyWords=&file=%2Fc1%2Fchuzhou%2FpublicInfoList_newest".format(
        #         i + 1) for i in range(3)]
        url_list_1 = [
            "https://www.chuzhou.gov.cn/chuzhou/site/label/8888?IsAjax=1&dataType=html&_=0.3740558893191772&labelName=publicInfoList&siteId=2653861&pageSize=20&pageIndex=1&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=152523227&type=4&catId=151969574&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&title=&fileNum=&keyWords=&file=%2Fc1%2Fchuzhou%2FpublicInfoList_newest"]
        url_list_2 = [
            "https://www.chuzhou.gov.cn/chuzhou/site/label/8888?IsAjax=1&dataType=html&_=0.7388437215457755&labelName=publicInfoList&siteId=2653861&pageSize=20&pageIndex=1&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=152523227&type=4&catId=151969595&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&title=&fileNum=&keyWords=&file=%2Fc1%2Fchuzhou%2FpublicInfoList_newest"]

        yield from HandleRequest().Get(self.parse,url_list_1,self.start_urls[0],"首页>信息公开>滁州市人民政府办公室>三大攻坚战>污染防治（生态环境领域）>建设项目环境影响评价","5E69E3A99C")
        yield from HandleRequest().Get(self.parse,url_list_2,self.start_urls[1],"首页 > 信息公开 > 滁州市人民政府办公室 > 三大攻坚战 > 污染防治（生态环境领域） > 生态建设","B32FE6FA6E")

    def handle_request(self, url_list,site_path_url):
        lua = """
                   function main(splash,args)
                     local url=args.url
                     splash:set_user_agent("Mozilla/5.0Chrome/69.0.3497.100Safari/537.36")
                     splash:go(url)
                     splash:wait(2)
                     splash:go(url)
                     return{
                     html=splash:html()
                     }
                   end
                   """
        for url in url_list:
            yield scrapy_splash.SplashRequest(
                url=url,
                callback=self.parse,
                endpoint="execute",
                args={
                    "lua_source": lua,
                    "url": url
                },
                meta={"site_path_url": copy.deepcopy(site_path_url)}
            )

    def parse(self, response, **kwargs):
        item = GetData().data_get(response)
        title_list = response.xpath('/html/body/div[1]/ul/li')
    #     # lua = """
    #     #        function main(splash, args)
    #     #          splash:go(args.url)
    #     #          local scroll_to = splash:jsfunc("window.scrollTo")
    #     #          scroll_to(0, 2800)
    #     #          splash:set_viewport_full()
    #     #          splash:wait(5)
    #     #          return {html=splash:html()}
    #     #        end
    #     #         """
        for li in title_list:
            item["title_url"] = li.xpath('./a/@href').extract_first()
            item['title_name'] = li.xpath('./a/@title').extract_first()
            item['title_date'] = li.xpath('./span/text()').extract_first()
            item['site_path_url'] = response.meta.get("site_path_url")
            yield scrapy.Request(
                url=item['title_url'],
                # endpoint="execute",
                callback=self.parse_detail,
                # args={
                #     "lua_source": lua,
                #     "url": item['title_url'],
                # },
                meta={'item': copy.deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item["content_html"] = response.xpath('//*[@class="wenzhang bg"]').extract_first()
        if item['content_html'] is None:
            item['content_html'] = response.text


        yield item

if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()
