"""

合肥市自然资源和规划局

"""
import scrapy

from PostCrawl.utils.data_get import GetData


class HefeinatureresourceproSpider(scrapy.Spider):
    name = 'HeFeiNatureResourcePro'
    # allowed_domains = ['xx.com']
    start_urls = ['http://zrzyhghj.hefei.gov.cn/public/column/13081?type=4&catId=6717321&action=list&nav=3',
                  'https://zwgk.hefei.gov.cn/public/column/13081?type=4&catId=6996361&action=list',
                  ]
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
        yield from self.gd.splash_query_get(self.parse, self.lua, [
            "https://zwgk.hefei.gov.cn/public/column/13081?type=4&catId=6996361&action=list"],
                                            "https://zwgk.hefei.gov.cn/public/column/13081?type=4&catId=6996361&action=list",
                                            site_path_name='首页>信息公开>合肥市自然资源和规划局>政策法规>部门文件',
                                            site_id='6A96B16D91')
        yield from self.gd.splash_query_get(self.parse, self.lua, [
            "http://zrzyhghj.hefei.gov.cn/public/column/13081?type=4&catId=6717321&action=list&nav=3"],
                                            "http://zrzyhghj.hefei.gov.cn/public/column/13081?type=4&catId=6717321&action=list&nav=3",
                                            site_path_name='首页>信息公开>合肥市自然资源和规划局>公共资源配置信息>矿业权出让>出让公告',
                                            site_id='B588E1E5FE')

    def parse(self, response):

        tr_list = response.css("li.clearfix")
        for td in tr_list:
            item = self.gd.data_get(response)
            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] = "http://zrzyhghj.hefei.gov.cn" + str(td.css("a::attr(href)").get())

            item['title_date'] = td.css("span::text").get()

            yield from self.gd.splash_detail_query_get(item, lua=self.lua, callback=self.parse_detail)



    def parse_detail(self, response):
        yield from self.gd.detail_get_data(response, ".gk_container.gkwz_container")


if __name__ == '__main__':
    GetData().crawler_run()