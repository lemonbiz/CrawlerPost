"""

包河区人民政府

"""

from copy import deepcopy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeibaoheareagovproSpider(scrapy.Spider):
    name = 'HeFeiBaoHeAreaGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://www.baohe.gov.cn/public/column/13771?type=4&action=list&nav=&sub=&catId=7006411']

    lua = """
               function main(splash, args)
                 splash:go(args.url)
                 local scroll_to = splash:jsfunc("window.scrollTo")
                 scroll_to(0, 2800)
                 splash:set_viewport_full()
                 splash:wait(5)
                 return {html=splash:html()}
               end
           """

    def start_requests(self):


        yield from self.handle_request(
            "http://www.baohe.gov.cn/public/column/13771?type=4&action=list&nav=&sub=&catId=7006411",
            "首页 > 信息公开 > 包河区人民政府（政府办公室） > “三大”攻坚战 > 污染防治（生态环境）",
            "BC33E6E6C9",
        )

    def handle_request(self, url, site_path_name, site_id):

        yield scrapy_splash.SplashRequest(
            url=url,
            endpoint="execute",
            callback=self.parse,
            args={
                "lua_source": self.lua,
                "url": url,
            },
            meta={
                "site_path_url": deepcopy(url),
                'site_path_name': deepcopy(site_path_name),
                'site_id': deepcopy(site_id)
            }
        )

    def parse(self, response):
        for li in response.css(".clearfix.xxgk_nav_list li"):
            item = GetData().data_get(response)
            item["title_url"] = "http://www.baohe.gov.cn" + str(li.css("a::attr(href)").get())
            item["title_name"] = li.css("a::attr(title)").get()
            item["title_date"] = li.css("span::text").get()
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                callback=self.parse_detail,
                args={
                    "lua_source": self.lua,
                    "url": item['title_url'],
                },
                meta={'item': deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item["content_html"] = response.css(".gk_container.gkwz_container").extract_first()

        if item['content_html'] is None:
            item['content_html'] = response.css("body").extract_first()
        yield item


if __name__ == '__main__':
    GetData().crawler_run()
