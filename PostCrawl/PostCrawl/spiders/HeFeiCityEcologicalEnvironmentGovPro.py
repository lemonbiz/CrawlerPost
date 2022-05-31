"""

合肥市生态环境局

"""

from copy import deepcopy

import httpx
import scrapy
import re
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeicityecologicalenvironmentgovproSpider(scrapy.Spider):
    name = 'HeFeiCityEcologicalEnvironmentGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://sthjj.hefei.gov.cn/hbyw/hpsp/jsxmhpgs/index.html',
        'http://sthjj.hefei.gov.cn/hbzt/wqzt/hjdczxd/index.html',
        'http://sthjj.hefei.gov.cn/hbzx/gsgg/index.html',
        'http://sthjj.hefei.gov.cn/site/tpl/13847?m=HPGGGS',
        'http://sthjj.hefei.gov.cn/site/tpl/13847?m=HPSL',
    ]

    def start_requests(self):
        url_jsxmhpgs = ["http://sthjj.hefei.gov.cn/content/column/6800451?pageIndex=1"]
        url_hjdczxd = ["http://sthjj.hefei.gov.cn/content/column/6816211?pageIndex=1"]
        url_gsgg = ["http://sthjj.hefei.gov.cn/content/column/6800221?pageIndex=1"]
        url_HPGGGS = ["http://sthjj.hefei.gov.cn/site/tpl/13847?m=HPGGGS&pageIndex=1"]
        url_HPSL = ["http://sthjj.hefei.gov.cn/site/tpl/13847?m=HPSL&pageIndex=1"]

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

        yield from self.handle_request(self.parse,
                                       lua,
                                       url_jsxmhpgs,
                                       "http://sthjj.hefei.gov.cn/hbyw/hpsp/jsxmhpgs/index.html",
                                       site_path_name='网站首页>环保业务>环评审批>建设项目环评公示',
                                       site_id='90CF3C9DE8')
        yield from self.handle_request(self.parse,
                                       lua,
                                       url_hjdczxd,
                                       "http://sthjj.hefei.gov.cn/hbzt/wqzt/hjdczxd/index.html",
                                       site_path_name='网站首页>环保专栏>往期专题>生态环保督察在行动',
                                       site_id='CC51776B49')
        yield from self.handle_request(self.parse,
                                       lua,
                                       url_gsgg,
                                       "http://sthjj.hefei.gov.cn/hbzx/gsgg/index.html",
                                       site_path_name='网站首页>环保资讯>公示公告',
                                       site_id='5D869ACC79')
        yield from self.handle_request(self.parse_HPSL,
                                       lua,
                                       url_HPGGGS,
                                       "http://sthjj.hefei.gov.cn/site/tpl/13847?m=HPGGGS",
                                       site_path_name='网站首页>在线服务>已批复项目公告',
                                       site_id='68D05A470E')
        yield from self.handle_request(self.parse_HPSL,
                                       lua,
                                       url_HPSL,
                                       "http://sthjj.hefei.gov.cn/site/tpl/13847?m=HPSL",
                                       site_path_name='网站首页>在线服务>建设项目环评受理公示',
                                       site_id='3F759726D7')

    def handle_request(self, callback, lua, url_list, site_path_url, site_path_name, site_id):
        for url in url_list:
            yield scrapy_splash.SplashRequest(
                url=url,
                endpoint="execute",
                callback=callback,
                args={
                    "lua_source": lua,
                    "url": url,
                },
                meta={
                    "site_path_url": deepcopy(site_path_url),
                    'site_path_name': deepcopy(site_path_name),
                    'site_id': deepcopy(site_id)

                }
            )

    def parse(self, response, **kwargs):

        item = GetData().data_get(response)
        title_ul = response.xpath('/html/body/div[2]/div/div[3]/div[3]/ul/li/a')
        date_ul = response.xpath('/html/body/div[2]/div/div[3]/div[3]/ul/li/span')

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
        for li, date in zip(title_ul, date_ul):
            item['title_url'] = li.xpath('./@href').extract_first()
            item['title_name'] = li.xpath('./@title').extract_first()
            item['title_date'] = date.xpath('./text()').extract_first()
            item['site_path_url'] = response.meta.get("site_path_url")

            # item['title_url'] = "http://sthjj.hefei.gov.cn/" + str(li.xpath('./@href').extract_first())
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                callback=self.parse_detail,
                args={
                    "lua_source": lua,
                    "url": item['title_url'],
                },
                meta={'item': deepcopy(item)},
            )

    def parse_HPSL(self, response, **kwargs):

        item = GetData().data_get(response)

        title_ul = response.xpath('/html/body/div[2]/div/div[3]/div[3]/ul/li/a')
        date_ul = response.xpath('/html/body/div[2]/div/div[3]/div[3]/ul/li/span')

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
        for li, date in zip(title_ul, date_ul):
            title_url = li.xpath('./@href').extract_first()
            if "http" in title_url:
                item['title_url']= title_url
            else:
                item['title_url'] = "http://sthjj.hefei.gov.cn/" + str(title_url)
            item['title_name'] = li.xpath('./@title').extract_first()
            item['title_date'] = date.xpath('./text()').extract_first()
            item['site_path_url'] = response.meta.get("site_path_url")

            # item['title_url'] = "http://sthjj.hefei.gov.cn/" + str(li.xpath('./@href').extract_first())
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                callback=self.parse_detail,
                args={
                    "lua_source": lua,
                    "url": item['title_url'],
                },
                meta={'item': deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item["content_html"] = response.xpath("/html/body/div[2]/div").extract_first()

        if item['content_html'] is None:
            item['content_html'] = response.text
        yield item


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()
