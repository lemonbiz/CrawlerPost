"""

山西省招标投标公共服务平台

"""
from copy import deepcopy

import scrapy



class ShanxiprovincetenderingbiddingproSpider(scrapy.Spider):
    name = 'ShanXiProvinceTenderingBiddingPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
                  'http://www.sxbid.com.cn/f/new/list-eee79988311d4f17b6c4de7b26f6c439.html',
                  'http://www.sxbid.com.cn/f/new/notice/list/10',
                  'http://www.sxbid.com.cn/f/new/notice/list/11',
                  'http://www.sxbid.com.cn/f/new/notice/list/12',
                  'http://www.sxbid.com.cn/f/new/notice/list/13',
                  'http://www.sxbid.com.cn/f/new/notice/list/14',
    ]

    def start_requests(self):
        yield scrapy.Request(
            url=f"http://www.sxbid.com.cn/f/new/list-eee79988311d4f17b6c4de7b26f6c439.html?pageNo=1&pageSize=15",
            callback=self.parse,
            meta={
                "site_path_url": deepcopy(self.start_urls[0]),
                "site_id": deepcopy("6BDE28BB63"),
                "site_path_name": deepcopy("首页>新闻动态>项目信息"),
            },

        )

        yield from self.handle_request("http://www.sxbid.com.cn/f/new/notice/list/10",self.start_urls[1],"招标信息>资格预审公告","5E42F33A4D")
        yield from self.handle_request("http://www.sxbid.com.cn/f/new/notice/list/11",self.start_urls[2],"首页>招标信息","439DC73428")
        yield from self.handle_request("http://www.sxbid.com.cn/f/new/notice/list/12",self.start_urls[3],"首页>招标信息","AFD91A3F05	")
        yield from self.handle_request("http://www.sxbid.com.cn/f/new/notice/list/13",self.start_urls[4],"首页>招标信息","4E7810D39A	")
        yield from self.handle_request("http://www.sxbid.com.cn/f/new/notice/list/14",self.start_urls[5],"首页>招标信息","C92409EF6B")

        # ********************全部爬取********************全部爬取********************全部爬取********************

        # for i in range(1, 698):
        #     yield scrapy.Request(
        #         url=f"http://www.sxbid.com.cn/f/new/list-eee79988311d4f17b6c4de7b26f6c439.html?pageNo={i}&pageSize=15",
        #         callback=self.parse
        #     )

        # for i in range(1,1001):
        #     yield scrapy.FormRequest(
        #         url="http://www.sxbid.com.cn/f/new/notice/list/11",
        #         formdata={
        #             "pageNo":  str(i),
        #             "pageSize": "15",
        #             "title": "",
        #             "recentType": "",
        #         },
        #         callback= self.parse_notice
        #     )
        #
        # for i in range(1,1001):
        #     yield scrapy.FormRequest(
        #         url="http://www.sxbid.com.cn/f/new/notice/list/12",
        #         formdata={
        #             "pageNo": str(i),
        #             "pageSize": "15",
        #             "title": "",
        #             "recentType": "",
        #         },
        #         callback= self.parse_notice
        #     )
        #
        # for i in range(1,1001):
        #     yield scrapy.FormRequest(
        #         url="http://www.sxbid.com.cn/f/new/notice/list/13",
        #         formdata={
        #             "pageNo":  str(i),
        #             "pageSize": "15",
        #             "title": "",
        #             "recentType": "",
        #         },
        #         callback= self.parse_notice
        #     )
        #
        # for i in range(1,1001):
        #     yield scrapy.FormRequest(
        #         url="http://www.sxbid.com.cn/f/new/notice/list/14",
        #         formdata={
        #             "pageNo":  str(i),
        #             "pageSize": "15",
        #             "title": "",
        #             "recentType": "",
        #         },
        #         callback= self.parse_notice
        #     )

    def handle_request(self,url,site_path_url,site_path_name,site_id):
        yield scrapy.FormRequest(
            url=url,
            formdata={
                "pageNo": "1",
                "pageSize": "15",
                "title": "",
                "recentType": "",
            },
            callback=self.parse_notice,
            meta={
                "site_path_url": deepcopy(site_path_url),
                "site_path_name": deepcopy(site_path_name),
                "site_id": deepcopy(site_id),
            }
        )

    def parse_notice(self,response):
        item = {}

        for tr in response.css("div.listBody.bg_panel table tr"):
            title_url: str = tr.css("td.text_left a::attr(href)").get()

            item['title_url'] = "http://www.sxbid.com.cn/" + str(title_url)
            item['title_name'] = tr.css("td.text_left a::attr(title)").get()
            item['title_date'] = tr.css("td:nth-child(3)::text").get()
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail_notice,
                meta={
                    "item": deepcopy(item)
                }
            )


    def parse_detail_notice(self, response):
        item = response.meta.get("item")

        item['content_html'] = response.css(".page_panel.noticeInfoDiv").get()

        yield item

    def parse(self, response, **kwargs):
        item = {}
        for tr in response.css("div.listBody.bg_panel table.content_table tr"):
            title_url: str = tr.css("td a::attr(href)").get()

            item['title_url'] = "http://www.sxbid.com.cn/" + title_url
            item['title_name'] = tr.css("td a::attr(title)").get()
            item['title_date'] = tr.css("td:nth-child(2)::text").get()
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )

    def parse_detail(self, response):
        item = response.meta.get("item")

        item['content_html'] = response.css(".page_panel").get()

        yield item
