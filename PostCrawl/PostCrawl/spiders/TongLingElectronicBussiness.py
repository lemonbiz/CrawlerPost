import re
import time
from copy import deepcopy

import scrapy
from ..utils.data_get import GetData


class TonglingelectronicbussinessSpider(scrapy.Spider):
    name = 'TongLingElectronicBussiness'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://tlchemshop.youzhicai.com/main/tend?NoticeType=2',
        'https://tlchemshop.youzhicai.com/main/tend?NoticeCateId=2&NoticeType=1',
        'https://tlchemshop.youzhicai.com/main/tend?NoticeCateId=1&NoticeType=1',
    ]

    def start_requests(self):

        for i in range(1,3):
            yield scrapy.FormRequest(
                url="https://tlchemshop.youzhicai.com/main/tend",
                formdata={
                    "keyword": "",
                    "publishDateStart": "",
                    "publishDateEnd": "",
                    "PageIndex": str(i),
                    "PageSize": "12",
                    "NoticeCateId": "",
                    "NoticeType": "2",
                    "ChildCompanyId": "",
                    "isMain": "0",
                },
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy("https://tlchemshop.youzhicai.com/main/tend?NoticeType=2"),
                    "site_path_name": deepcopy("铜化专区>项目信息>结果公示"),
                    "site_id": deepcopy("0C37CCE6EA"),
                },
                dont_filter=True,
            )

        for i in range(1, 3):
            yield scrapy.FormRequest(
                url="https://tlchemshop.youzhicai.com/main/tend",
                formdata={
                    "keyword": "",
                    "publishDateStart": "",
                    "publishDateEnd": "",
                    "TenderType": "全部",
                    "PageIndex": str(i),
                    "PageSize": "12",
                    "NoticeCateId": "2",
                    "NoticeType": "1",
                    "ChildCompanyId": "",
                    "isMain": "0",
                },
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy("https://tlchemshop.youzhicai.com/main/tend?NoticeCateId=2&NoticeType=1"),
                    "site_path_name": deepcopy("首页铜化专区>非招标业务>"),
                    "site_id": deepcopy("47DA3FA525"),
                },
                dont_filter=True,
            )

        for i in range(1, 3):
            yield scrapy.FormRequest(
                url="https://tlchemshop.youzhicai.com/main/tend",
                formdata={
                    "keyword": "",
                    "publishDateStart": "",
                    "publishDateEnd": "",
                    "TenderType": "全部",
                    "PageIndex": str(i),
                    "PageSize": "12",
                    "NoticeCateId": "1",
                    "NoticeType": "1",
                    "ChildCompanyId": "",
                    "isMain": "0",
                },
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy("https://tlchemshop.youzhicai.com/main/tend?NoticeCateId=1&NoticeType=1"),
                    "site_path_name": deepcopy("铜化专区>招标业务>采购公告"),
                    "site_id": deepcopy("18CF5632CB"),
                },
                dont_filter=True,
            )

    def parse(self, response, **kwargs):
        gd = GetData()
        for li in response.css("ul.special_tabmain li"):
            item = gd.data_get(response)
            item["title_url"] = "http:"+li.css("span a::attr(href)").get()
            item["title_name"] = li.css("span a::attr(title)").get()

            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )

    def parse_detail(self, response):
        item = response.meta['item']
        try:
            item['title_date'] = re.findall("(\d{4}-\d{2}-\d{2})", response.body.decode(response.encoding))[0]
        except:
            item['title_date'] = time.strftime('%Y-%m-%d')
        item['content_html'] = response.css(".Container.content.clearfix").get()
        yield item



