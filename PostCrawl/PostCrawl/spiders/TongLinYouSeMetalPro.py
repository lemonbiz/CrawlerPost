"""

铜陵有色集团电子采购（招投标）系统

"""
import re
import time
from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData


class TonglinyousemetalproSpider(scrapy.Spider):
    name = 'TongLinYouSeMetalPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://ec.tlys.cn:10000/main/TradingNotices?type=4&noticetype=1',
        'https://ec.tlys.cn:10000/main/TradingNotices?type=2&noticetype=1',
        'https://ec.tlys.cn:10000/main/TradingNotices?type=2&noticetype=2',
        'https://ec.tlys.cn:10000/main/TradingNotices?type=1&noticetype=2',
        'https://ec.tlys.cn:10000/main/TradingNotices?type=1&noticetype=1',

    ]

    def start_requests(self):
        # yield from self.handle_request(_type="4", noticetype="1", site_path_url=self.start_urls[0],
        #                                site_path_name="设备物资> 竞价采购>竞价公告", site_id="1CC4955436")
        # yield from self.handle_request(_type="2", noticetype="1", site_path_url=self.start_urls[1],
        #                                site_path_name="建设工程> 招标公告>", site_id="C034D982DE")
        yield from self.handle_request(_type="2", noticetype="2", site_path_url=self.start_urls[2],
                                       site_path_name="建设工程>中标公告", site_id="4FEA97D81B")
        # yield from self.handle_request(_type="1", noticetype="2", site_path_url=self.start_urls[3],
        #                                site_path_name="设备物资> 招标采购>中标公告", site_id="189520AC84")
        # yield from self.handle_request(_type="1", noticetype="1", site_path_url=self.start_urls[4],
        #                                site_path_name="设备物资> 招标采购>招标公告", site_id="543586B974")

    def handle_request(self, _type: str, noticetype: str, site_path_url, site_path_name, site_id):
        yield scrapy.FormRequest(
            url="https://ec.tlys.cn:10000/main/TradingNotices",
            formdata={
                "keyword": "",
                "startdate": "",
                "enddate": "",
                "type": _type,
                "noticetype": noticetype,
                "PageIndex": "1",
                "PageSize": "10",
            },
            callback=self.parse,
            meta={
                "site_path_url": site_path_url,
                "site_path_name": site_path_name,
                "site_id": site_id,
            },
            dont_filter=True
        )

    def parse(self, response,**kwargs):
        gd = GetData()

        for li in response.css(".main ul li"):
            onclick: str = li.css("li::attr(onclick)").get()

            item = gd.data_get(response)
            item["title_name"] = li.css("p::text").get()

            url_id = re.search(r"NoticeDetail\('(.*)','", onclick).group(1)
            item['title_url'] = f"https://ec.tlys.cn:10000/main/NoticeDetails?id={url_id}&cate=2&"

            yield scrapy.Request(
                url=item['title_url'],

                callback=self.parse_detail,

                meta={
                    "item": deepcopy(item)
                },
                dont_filter=True,
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css(".main.clearfix").get()
        try:
            item['title_date'] = re.findall("(\d{4}-\d{2}-\d{2})", response.text)[0]
        except:
            item['title_date'] = time.strftime('%Y-%m-%d %H:%M:%S')

        yield item