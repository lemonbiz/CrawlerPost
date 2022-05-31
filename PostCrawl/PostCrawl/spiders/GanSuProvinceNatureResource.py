"""



"""
import copy
import json
import scrapy
import scrapy_splash

from PostCrawl.utils.Mixins import Mixins
from PostCrawl.utils.data_get import GetData


class GansuprovincenatureresourceSpider(scrapy.Spider):
    name = 'GanSuProvinceNatureResource'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://sthj.gansu.gov.cn/sthj/c105992/xxgk_list.shtml']
    #
    # def start_requests(self):
    #     url="http://sthj.gansu.gov.cn/common/search/7cfa6365343e4f69b13f0ade298c0580?_isAgg=true&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1"

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
        url = "http://sthj.gansu.gov.cn/sthj/c105992/xxgk_list.shtml"
        yield from self.handle_request(url, self.before_parse)

    def handle_request(self, url,next_func):
        yield scrapy_splash.SplashRequest(
            url=url,
            callback=next_func,
            endpoint="execute",
            args={
                "lua_source": self.lua,
                "url": url,
            }

        )

    def before_parse(self, response):

        channelId = response.css("meta[name=channelId]::attr(content)").get()
        # for i in range(1,23):
        #     url = f"http://sthj.gansu.gov.cn/common/search/{channelId}?_isAgg=true&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={i}"
        #     yield from self.handle_request(url,self.parse)
        url = f"http://sthj.gansu.gov.cn/common/search/{channelId}?_isAgg=true&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1"
        yield from self.handle_request(url,self.parse)

    def parse(self, response,**kwargs):
        item = GetData().data_get(response)
        # 转换为json格式
        page_text = response.xpath("/html/body/pre/text()[1]").extract_first()
        json_text=json.loads(page_text)
        for item1 in json_text["data"]['results']:
            url = item1['url']
            date = item1['publishedTimeStr']
            title_name = item1['title']
            # print(url,"**",date,"**",title_name,)
            item['site_path_url'] = self.start_urls[0]
            # 链接补全
            item['title_url'] = Mixins().Get_domain_name(item['site_path_url'],url)
            item['title_name'] = str(title_name)
            item['title_date'] = str(date)

            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                callback=self.parse_detail,
                endpoint="execute",
                args={
                    "lua_source": self.lua,
                    "url": item['title_url'],
                },

                meta={
                    "item": copy.deepcopy(item)
                }
            )
    def parse_detail(self, response):
        item = response.meta['item']
        item["content_html"] = response.css('body > div.inner > div > div.mainside').get()
        item['site_path_name'] = "首页>政府信息公开>法定主动公开内容>重点领域信息公开>建设项目环评>批准项目公告"
        item['site_id'] = "C819612177"
        yield item


if __name__ == '__main__':
    import os
    os.system("scrapy crawl GanSuNatureResourcePro")
