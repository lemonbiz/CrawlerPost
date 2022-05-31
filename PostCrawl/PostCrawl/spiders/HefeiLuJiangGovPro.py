import copy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeilujianggovproSpider(scrapy.Spider):
    name = 'HefeiLuJiangGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://www.lj.gov.cn/public/column/13721?type=4&action=list&nav=3&sub=&catId=7006411']

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
        url = [f"http://www.lj.gov.cn/public/column/13721?sub=&catId=7006411&nav=3&action=list&type=4&pageIndex={i}"for i in range(1,50)]
        yield from self.gd.splash_query_get(self.parse, self.lua, url, self.start_urls[0],
                                            site_path_name='首页 > 信息公开 > 庐江县人民政府（政府办公室） > “三大”攻坚战 > 污染防治（生态环境）',
                                            site_id='494E35BFAF')


    def parse(self, response, **kwargs):
        tr_list = response.css("li.clearfix")
        for td in tr_list:
            item = self.gd.data_get(response)
            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] ="http://www.lj.gov.cn"+str(td.css("a::attr(href)").get())

            item['title_date'] = td.css("span::text").get()

            yield from self.gd.splash_detail_query_get(item,lua=self.lua,callback=self.parse_detail)


    def parse_detail(self, response):
        yield from self.gd.detail_get_data(response,".gk_container.gkwz_container")

if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()
