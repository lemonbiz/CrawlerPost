import copy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeilujianggovproSpider(scrapy.Spider):
    name = 'HefeiLuJiangGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://www.lj.gov.cn/public/column/13721?type=4&action=list&nav=3&sub=&catId=7006411',
        'http://www.lj.gov.cn/zwdt/gsgg/index.html',
        'http://www.lj.gov.cn/zwdt/zwdt/index.html',
        'http://www.lj.gov.cn/public/column/13721?type=4&catId=7004271&action=list',

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

        yield from self.gd.splash_query_get(self.parse, self.lua, [
            f"http://www.lj.gov.cn/public/column/13721?sub=&catId=7006411&nav=3&action=list&type=4&pageIndex=1"],
                                            self.start_urls[0],
                                            site_path_name='首页 > 信息公开 > 庐江县人民政府（政府办公室） > “三大”攻坚战 > 污染防治（生态环境）',
                                            site_id='494E35BFAF')
        yield from self.gd.splash_query_get(self.parse_1, self.lua,
                                            ['http://www.lj.gov.cn/content/column/11245557?pageIndex=1'],
                                            self.start_urls[1],
                                            site_path_name='首页>政务动态>公示公告',
                                            site_id='5D9D5531A0')
        yield from self.gd.splash_query_get(self.parse_1,
                                            self.lua,
                                            ['http://www.lj.gov.cn/content/column/26279122?pageIndex=1'],
                                            self.start_urls[2],
                                            site_path_name='首页>政务动态>政务动态',
                                            site_id='FFA638B723')
        yield from self.gd.splash_query_get(self.parse,
                                            self.lua,
                                            [
                                                'http://www.lj.gov.cn/public/column/13721?type=4&catId=7004271&action=list'],
                                            self.start_urls[3],
                                            site_path_name='首页 > 信息公开 > 庐江县人民政府（政府办公室） > 公共资源配置信息 > 矿业权出让',
                                            site_id='6F5EC82CE1')

    def parse(self, response, **kwargs):
        tr_list = response.css("li.clearfix")
        for td in tr_list:
            item = self.gd.data_get(response)
            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] = "http://www.lj.gov.cn" + str(td.css("a::attr(href)").get())

            item['title_date'] = td.css("span::text").get()

            yield from self.gd.splash_detail_query_get(item, lua=self.lua, callback=self.parse_detail)

    def parse_detail(self, response):
        yield from self.gd.detail_get_data(response, ".gk_container.gkwz_container")

    def parse_1(self, response, **kwargs):

        # if response.meta['site_id'] == "FFA638B723":
        #     tr_list = response.css(".doc_list.list-26279122 li")
        # else:
        #     tr_list = response.css(".doc_list.list-11245557 li")

        for td in response.css(".doc_list li"):
            item = self.gd.data_get(response)
            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] = "http://www.lj.gov.cn" + str(td.css("a::attr(href)").get())

            item['title_date'] = td.css("span::text").get()
            print(item)
            yield from self.gd.splash_detail_query_get(item, lua=self.lua, callback=self.parse_detail_1)

    def parse_detail_1(self, response):
        yield from self.gd.detail_get_data(response, "#color_printsssss")


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()
