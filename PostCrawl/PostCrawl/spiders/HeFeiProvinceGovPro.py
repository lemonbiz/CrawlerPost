"""

合肥市人民政府

"""
import scrapy

from PostCrawl.utils.data_get import GetData


class HefeiprovincegovproSpider(scrapy.Spider):
    name = 'HeFeiProvinceGovPro'
    # allowed_domains = ['xx.com']
    start_urls = ['https://zwgk.hefei.gov.cn/public/column/1741?type=4&action=list&nav=3&sub=&catId=6977231']

    gd = GetData()

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
        yield from self.gd.splash_query_get(self.parse, self.lua, ["https://zwgk.hefei.gov.cn/public/column/1741?type=4&action=list&nav=3&sub=&catId=6977231"],
                                            "https://zwgk.hefei.gov.cn/public/column/1741?type=4&action=list&nav=3&sub=&catId=6977231",
                                            site_path_name='首页>信息公开>合肥市人民政府（政府办公室）>“三大”攻坚战>污染防治（生态环境）',
                                            site_id='E2EA2AA362')

    def parse(self, response):
        tr_list = response.css("li.clearfix")
        item = self.gd.data_get(response)
        for td in tr_list:

            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] = "https://zwgk.hefei.gov.cn" + str(td.css("a::attr(href)").get())

            item['title_date'] = td.css("span::text").get()
            yield from self.gd.splash_detail_query_get(item, lua=self.lua, callback=self.parse_detail)

    def parse_detail(self, response):
        yield from self.gd.detail_get_data(response, ".gk_container.gkwz_container")


if __name__ == '__main__':
    GetData().crawler_run()