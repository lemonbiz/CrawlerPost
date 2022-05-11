"""
	铜陵有色金属集团控股有限公司

"""
from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData


class TonglinyousemetalOldproSpider(scrapy.Spider):
    name = 'TongLinYouSeMetal_oldPro'
    # allowed_domains = ['xx.com']
    start_urls = [
        'http://www.tnmg.com.cn/information/info_zxzb.aspx?classid=411&classname=%e6%8b%9b%e6%a0%87%e5%85%ac%e5%91%8a',
    ]


    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={
                "site_path_url": deepcopy(self.start_urls[0]),
                "site_path_name": deepcopy("在线招标>设备物资>招标公告"),
                "site_id": deepcopy("1506EB7D68"),
            },
        )

    def parse(self, response):
        __EVENTTARGET = "GridView1$ctl23$KXPortal_Pager1$btnNext"
        __EVENTARGUMENT = ""

        __VIEWSTATE = response.css("#__VIEWSTATE::attr(value)").get()
        __VIEWSTATEGENERATOR = response.css("#__VIEWSTATEGENERATOR::attr(value)").get()
        __VIEWSTATEENCRYPTED = ""
        __EVENTVALIDATION = response.css("#__EVENTVALIDATION::attr(value)").get()

        item = GetData().data_get(response)

        for tr in response.css("#GridView1 tr"):
            item["title_url"] = tr.css("td a::attr(href)").get()
            item["title_name"] = tr.css("td a::text").get()
            item["title_date"] = tr.css("td:nth-child(2)::text").get()
            if item['title_date'] is None:
                continue
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )

        yield scrapy.FormRequest(
            url="http://www.tnmg.com.cn/information/info_zxzb.aspx?classid=411&classname=%u62db%u6807%u516c%u544a",
            formdata={
                "__EVENTTARGET":__EVENTTARGET,
                "__EVENTARGUMENT":__EVENTARGUMENT,
                "__VIEWSTATE":__VIEWSTATE,
                "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
                "__EVENTVALIDATION":__EVENTVALIDATION,
                "__VIEWSTATEENCRYPTED":__VIEWSTATEENCRYPTED
            },
            callback=self.parse,
            dont_filter=True,
            meta={
                "site_path_url": deepcopy(self.start_urls[0]),
                "site_path_name": deepcopy("在线招标>设备物资>招标公告"),
                "site_id": deepcopy("1506EB7D68"),
            }
        )

    def parse_detail(self,response):
        item =response.meta['item']
        item['content_html'] = response.css(".main.clearfix").get()
        print(item['site_path_url'],item['site_path_name'],item['title_url'])
        yield item