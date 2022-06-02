from copy import deepcopy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeichaohugovproSpider(scrapy.Spider):
    name = 'HeFeiChaoHuGovPro'
    # allowed_domains = ['']
    start_urls = [
        'https://zwgk.hefei.gov.cn/public/column/14081?type=4&catId=7001011&action=list',
        "https://zwgk.hefei.gov.cn/public/column/13731?type=4&action=list&nav=3&sub=&catId=7003771",
        'https://www.chaohu.gov.cn/public/column/13961?type=4&catId=6999451&action=list',


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

    def start_requests(self):

        yield from self.handle_request(
            "https://zwgk.hefei.gov.cn/public/column/14081?type=4&catId=7001011&action=list",
            "首页 > 信息公开 > 巢湖市经济和信息化局 > “三大”攻坚战 > 防范化解重大风险 > 措施及成效",
            "349A7CA951",
        )

        yield from self.handle_request(
            "https://zwgk.hefei.gov.cn/public/column/13731?type=4&action=list&nav=3&sub=&catId=7003771",
            "您当前所在位置：首页 > 信息公开 > 巢湖市人民政府（政府办公室） > 重大建设项目批准和实施 > 批准结果信息",
            "F24ECF1431",
        )

        yield from self.handle_request(
            "https://www.chaohu.gov.cn/public/column/13961?type=4&catId=6999451&action=list",
            "首页 > 信息公开 > 巢湖市生态环境分局 > 社会公益事业建设 > 环境保护 > 建设项目环境影响评价审批",
            "1E30BD775B",
        )

    def handle_request(self,url,site_path_name,site_id):

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
            item["title_url"] = "https://zwgk.hefei.gov.cn/" + str(li.css("a::attr(href)").get())
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
