"""

湖北省自然资源厅

"""
from copy import deepcopy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HubeinaturalresourcegovproSpider(scrapy.Spider):
    name = 'HuBeiNaturalResourceGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://zrzyt.hubei.gov.cn/fbjd/zhengce/qtzdgkwj/']

    def start_requests(self):
        yield from self.handle_request(
            callback=self.parse,
            url="http://zrzyt.hubei.gov.cn/fbjd/zhengce/qtzdgkwj/list.json",
            site_path_url="http://zrzyt.hubei.gov.cn/fbjd/zhengce/qtzdgkwj/",
            site_path_name="首页>政府信息公开>政策>其他主动公开文件",
            site_id="0C3C53C55B",
        )
        yield from self.handle_request(
            callback=self.parse_1,
            url="http://sthjt.hubei.gov.cn/fbjd/zc/zcwj/2022qtzdgk.json",
            site_path_url="http://sthjt.hubei.gov.cn/fbjd/zc/zcwj/sthjt/ehf/",
            site_path_name="首页>政府信息公开>政策>其他主动公开文件",
            site_id="A4C3757857",
        )


    def handle_request(self,callback, url, site_path_url, site_path_name, site_id):
        yield scrapy.Request(
            url=url,
            callback=callback,
            meta={
                "site_path_url": deepcopy(site_path_url),
                "site_path_name": deepcopy(site_path_name),
                "site_id": deepcopy(site_id),
            },
        )

    lua=\
    """
    function main(splash,args)
          local url=args.url
          splash:set_user_agent("Mozilla/5.0Chrome/69.0.3497.100Safari/537.36")
          splash:go(url)
          splash:wait(2)
          splash:go(url)
          return{
          html=splash:html(),
          png = splash:png()
          }
    end
    
    """

    def parse(self, response):
        print(response.json())

        for data in response.json()['data']:
            item=GetData().data_get(response)
            item['title_url'] = data['URL']
            item['title_name'] = data['DOCTITLE']
            item['title_date'] = data['DOCRELTIME']

            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                args={
                    "url": item['title_url'],
                    "lua_source": self.lua,
                },
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )
    def parse_1(self, response):

        for data in response.json()['data']:
            item=GetData().data_get(response)
            item['title_url'] = data['url']
            item['title_name'] = data['DOCTITLE']
            item['title_date'] = data['PubDate']

            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                args={
                    "url": item['title_url'],
                    "lua_source": self.lua,
                },
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )

    def parse_detail(self,response):
        item = response.meta['item']
        item['content_html']: str = response.css(".main.mb20").get() or response.css(".article").get()
        yield item



if __name__ == '__main__':
    GetData().crawler_run()