"""

国家电网公司电子商务平台


"""

import copy
import json

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData

gd = GetData()


class StategridtenderannouncementSpider(scrapy.Spider):
    name = 'StateGridTenderAnnouncement'
    # allowed_domains = ['xxx.com']
    start_urls = ["https://ecp.sgcc.com.cn/ecp2.0/portal/#/list/list-com/2018032600000014_5_2018032700291334"]
    url = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'

    def start_requests(self):
        data = {
            'firstPageMenuId': '2018032700291334',
            'index': "1",
            'key': '',
            'orgId': '',
            'orgName': '',
            'purOrgCode': '',
            'purOrgStatus': '',
            'purType': '',
            'size': '20'
        }
        yield scrapy.Request(
            url=self.url,
            method='POST',
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            callback=self.parse,
            dont_filter=True,

            meta={
                "site_path_url": copy.deepcopy(self.start_urls[0]),
                "site_path_name": copy.deepcopy("首页>招标采购>招标公告"),
                "site_id": copy.deepcopy("701F6D17DE"),
            }

        )

    lua = """
    function main(splash, args)
          splash:go(args.url)
          local scroll_to = splash:jsfunc("window.scrollTo")
          scroll_to(0, 2800)
          splash:set_viewport_full()
          splash:wait(5)
          return {
        html=splash:html(),
        png = splash:png()}
    end
    """

    def parse(self, response, **kwargs):

        # 第二层post请求的内容页面的url
        for li in response.json()['resultValue']['noteList']:
            item = GetData().data_get(response)
            # 目标标题
            item['title_name'] = li['title']
            # 目标详情页的地址
            item['title_url'] = 'https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-change/' + str(
                li['id']) + '_2018032700291334'
            # 目标日期
            item['title_date'] = li['noticePublishTime']
            # print(item['title_name'], item['title_url'], item['title_date'])
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                args={
                    "url": item['title_url'],
                    "lua_source": self.lua,
                    "wait": 1
                },
                meta={
                    "item": copy.deepcopy(item)
                },
                callback=self.parse_content
            )

    def parse_content(self, response):  # 第二层页面解析，返回第二层详情页内容
        item = response.meta['item']
        item['content_html'] = response.css(".wrapper.gray").get()
        if item['content_html'] is None:
            item['content_html'] = str(response.body)
        yield item


if __name__ == '__main__':
    gd.crawler_run()
