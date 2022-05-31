"""

祁门县人民政府

"""
import copy
import re
import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HubeiecologicalenvironmentproSpider(scrapy.Spider):
    name = 'HuBeiEcologicalEnvironmentPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://yjt.hubei.gov.cn/yjgl/aqsc/fmks/index.shtml']

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

        # for url in ["http://yjt.hubei.gov.cn/yjgl/aqsc/fmks/index_{}.shtml".format(i+1)for i in range(28)]:
        for url in ['http://yjt.hubei.gov.cn/yjgl/aqsc/fmks/index.shtml']:

            yield scrapy_splash.SplashRequest(
                url=url,
                callback=self.parse,
                endpoint="execute",
                args={
                    "lua_source": self.lua,
                    "url": url
                }
            )
    def parse(self, response):
        item = {}
        title_list = response.css('.lsj-list ul li')

        for li in title_list:
            item['site_path_name'] = "首页>应急管理>安全生产>非煤矿山"
            item['site_id'] = "0717B475E6"
            item['site_path_url'] = self.start_urls[0]
            item["title_url"] = li.css('a::attr(href)').get()
            item['title_name'] = li.css('a::attr(title)').get()
            item['title_date'] = li.css('i::text').get()
            item['site_path_url'] = self.start_urls[0]
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                callback=self.parse_detail,
                args={
                    "lua_source": self.lua,
                    "url": item['title_url'],
                },
                meta={'item': copy.deepcopy(item)},
            )



    def parse_detail(self, response):
        item = response.meta['item']

        item["content_html"] = response.css(".article").extract_first()


        if item['content_html'] is None:
            item['content_html'] = response.text

        yield item

if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()