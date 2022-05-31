"""

合肥市自然资源市规划局

"""

import copy
import scrapy

import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeicitynatureresourceproSpider(scrapy.Spider):
    name = 'HeFeiCityNatureResourcePro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        "http://zrzyhghj.hefei.gov.cn/xwzx/bsdt/index.html",
        "http://zrzyhghj.hefei.gov.cn/xwzx/tzgg/index.html",
        "http://zrzyhghj.hefei.gov.cn/xwzx/ywlb/index.html",
    ]
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
    gd = GetData()

    def start_requests(self):
        url_part1 = ["http://zrzyhghj.hefei.gov.cn/content/column/6787391?pageIndex=1"]
        url_part2 = ["http://zrzyhghj.hefei.gov.cn/content/column/6787421?pageIndex=1"]
        url_part3 = ["http://zrzyhghj.hefei.gov.cn/content/column/6787381?pageIndex=1"]

        # url_part1 = ["http://zrzyhghj.hefei.gov.cn/content/column/6787391?pageIndex={}".format(i + 1) for i in
        #              range(25)]
        # url_part2 = ["http://zrzyhghj.hefei.gov.cn/content/column/6787421?pageIndex={}".format(i + 1) for i in
        #              range(25)]
        # url_part3 = ["http://zrzyhghj.hefei.gov.cn/content/column/6787381?pageIndex={}".format(i + 1) for i in
        #              range(25)]

        yield from self.gd.splash_query_get(self.parse,self.lua, url_part1, self.start_urls[0], site_path_name='首页>新闻中心>部省动态',
                                            site_id='FD559C39DD')
        yield from self.gd.splash_query_get(self.parse, self.lua,url_part2, self.start_urls[1], site_path_name='首页>新闻中心>通知公告',
                                            site_id='5A7D79EC8C')
        yield from self.gd.splash_query_get(self.parse,self.lua, url_part3, self.start_urls[2], site_path_name='首页>新闻中心>要闻联播',
                                            site_id='11689F0F63')

    def parse(self, response, **kwargs):
        tr_list = response.css(".listnews ul li")
        for td in tr_list:
            item = self.gd.data_get(response)
            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] = td.css("a::attr(href)").get()

            item['title_date'] = td.css("span::text").get()
            yield from self.gd.splash_detail_query_get(item,lua=self.lua,callback=self.parse_detail)

    def parse_detail(self, response):
        yield from self.gd.detail_get_data(response,'div.con_main')


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()
