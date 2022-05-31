"""

酒泉市公共资源交易中心

"""
import copy
import json
import jsonpath
import scrapy
import scrapy_splash
from PostCrawl.utils.data_get import GetData


class JiuquancitypublicresourceproSpider(scrapy.Spider):
    name = 'JiuQuanCityPublicResourcePro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://www.ggzyjypt.com.cn/jyxxgk/tradelist.html']

    def start_requests(self):
        yield scrapy.FormRequest(
            url="http://www.ggzyjypt.com.cn/EpointWebBuilder_jqggzy/getGgListAction.action?cmd=getZtbGgList",
            formdata={
                "pageIndex": "1",
                "pageSize": "20",
                "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
                "title": "",
                "categorynum": "008001",
                "diqu": "620901",
                "xmlx": "",
                "cgfs": "",
            },
            callback=self.parse
        )

    # def start_requests(self):
    #     for i in range(1,242):
    #         yield scrapy.FormRequest(
    #             url="http://www.ggzyjypt.com.cn/EpointWebBuilder_jqggzy/getGgListAction.action?cmd=getZtbGgList",
    #             formdata={
    #                 "pageIndex": "{}".format(i),
    #                 "pageSize": "20",
    #                 "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
    #                 "title": "",
    #                 "categorynum": "008001",
    #                 "diqu": "620901",
    #                 "xmlx": "",
    #                 "cgfs": "",
    #             },
    #             callback=self.parse
    #         )

    def parse(self, response, **kwargs):

        lua=\
        """
            function main(splash, args)
              splash:go(args.url)
              local scroll_to = splash:jsfunc("window.scrollTo")
              scroll_to(0, 2800) 
              splash:set_viewport_full()
              splash:wait(5)
              return {html=splash:html()}
            end
        """

        item = GetData().data_get(response)
        json_text = json.loads(response.text)

        json_inner_text = jsonpath.jsonpath(json_text, '$..custom')[0]
        json_inner_text = json.loads(json_inner_text)

        # 提取 id的值
        url_list = jsonpath.jsonpath(json_inner_text, '$..href')

        title_name_list = jsonpath.jsonpath(json_inner_text, '$..title')

        title_date_list = jsonpath.jsonpath(json_inner_text, '$..infodate')
        for url, title_name, title_date in zip(url_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item['title_url'] = str(
                'http://www.ggzyjypt.com.cn{}').format(
                url)
            item['site_path_url'] = self.start_urls[0]
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)},
                endpoint="execute",
                args={
                    "url": item['title_url'],
                    "lua_source": lua,
                },
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['site_path_url'] = self.start_urls[0]
        item['site_path_name'] = "首页>交易信息公开"
        item['site_id'] = "9EB2A40E01"

        item['content_html'] = response.css(".ewb-det").get()

        yield item


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()