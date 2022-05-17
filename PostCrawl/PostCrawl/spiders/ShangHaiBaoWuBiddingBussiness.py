"""

中国宝武采购专区/欧冶工业品

"""
import copy

import httpx
import jsonpath
import scrapy
import ujson

from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class ShanghaibaowubiddingbussinessSpider(scrapy.Spider):
    name = 'ShangHaiBaoWuBiddingBussiness'
    # allowed_domains = ['xxx.com']
    start_urls = [

        'http://baowu.ouyeelbuy.com/baowu-shp/moreLista.html',
        'http://baowu.ouyeelbuy.com/baowu-shp/moreListb.html',
        'http://baowu.ouyeelbuy.com/baowu-shp/notice/entrustPublicity.html',
    ]

    def start_requests(self):
        for i in range(1,10):
            yield scrapy.FormRequest(
                url="http://baowu.ouyeelbuy.com/baowu-shp/notice/purchaseMore?pageFlag=addSelect&pageSize=20",
                formdata={
                    "sDate": "",
                    "eDate": "",
                    "title": "",
                    "ouName": "",
                    "rfqMethod": "",
                    "cTeam": "",
                    "type": "purchase",
                    "pageNow": str(i),
                    "jqMthod": "newsList",
                },
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[0]),
                    "site_path_name": copy.deepcopy("采购公告"),
                    "site_id": copy.deepcopy("DC245BEA15"),
                },
                callback=self.parse_moreLista
            )
        for i in range(1,10):
            yield scrapy.FormRequest(
                url="http://baowu.ouyeelbuy.com/baowu-shp/notice/purchaseMore?pageFlag=addSelect&pageSize=20",
                formdata={
                    "sDate": "",
                    "eDate": "",
                    "title": "",
                    "ouName": "",
                    "rfqMethod": "",
                    "cTeam": "",
                    "type": "purchase",
                    "pageNow": str(i),
                    "jqMthod": "newsList",
                },
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[1]),
                    "site_path_name": copy.deepcopy("中标公告"),
                    "site_id": copy.deepcopy("02BE6D076E"),
                },
                callback=self.parse_moreListb
            )
        for i in range(1,10):
            yield scrapy.FormRequest(
                url="http://baowu.ouyeelbuy.com/baowu-shp/notice/moreEntrustPublicity",
                formdata={
                    "title": "",
                    "sDate": "",
                    "eDate": "",
                    "type": "",
                    "pageNow": str(i),
                    "jqMthod": "newsList",
                    "ouName": "",
                },
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[2]),
                    "site_path_name": copy.deepcopy("首页>委托公示"),
                    "site_id": copy.deepcopy("57586E200E"),
                }
            )

    # def start_requests(self):
    #     for i in range(1,5):
    #         yield scrapy.FormRequest(
    #             url="http://baowu.ouyeelbuy.com/baowu-shp/notice/moreEntrustPublicity",
    #             formdata={
    #                 "title": "",
    #                 "sDate": "",
    #                 "eDate": "",
    #                 "type": "",
    #                 "pageNow": str(i),
    #                 "jqMthod": "newsList",
    #                 "ouName": "",
    #             },
    #             callback=self.parse,
    #             meta={
    #                 "site_path_url": copy.deepcopy(self.start_urls[0])
    #             }
    #         )
    #     for i in range(1,5):
    #         yield scrapy.FormRequest(
    #             url="http://baowu.ouyeelbuy.com/baowu-shp/notice/bidMore?pageFlag=addSelect&pageSize=100",
    #             formdata={
    #                 "sDate": "",
    #                 "eDate": "",
    #                 "title": "",
    #                 "ouName": "",
    #                 "rfqMethod": "",
    #                 "cTeam": "",
    #                 "type": "bid",
    #                 "pageNow": str(i),
    #                 "jqMthod": "newsList",
    #             },
    #             meta={
    #                 "site_path_url": copy.deepcopy(self.start_urls[1])
    #             }
    #         )
    #
    #     for i in range(1, 5):
    #         yield scrapy.FormRequest(
    #             url="http://baowu.ouyeelbuy.com/baowu-shp/notice/bidMore?pageFlag=addSelect&pageSize=100",
    #             formdata={
    #                 "sDate": "",
    #                 "eDate": "",
    #                 "title": "",
    #                 "ouName": "",
    #                 "rfqMethod": "",
    #                 "cTeam": "",
    #                 "type": "purchase",
    #                 "pageNow": str(i),
    #                 "jqMthod": "newsList",
    #             },
    #             meta={
    #                 "site_path_url": copy.deepcopy(self.start_urls[2])
    #             }
    #         )

    def parse(self, response, **kwargs):
        item = {}
        json_text = ujson.loads(response.text)
        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..id')

        title_name_list = jsonpath.jsonpath(json_text, '$..projectName')

        title_date_list = jsonpath.jsonpath(json_text, '$..recCreateTime')

        for id1, title_name, title_date in zip(id1_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")

            item['title_url'] = f"http://rfq.ouyeelbuy.com/rfqNotice/entrustPublicityDetail?id={id1}&appCode=baowu"

            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)}
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item['content_html'] = response.css(".left-bodys").get()
        yield item

    def parse_moreLista(self, response, **kwargs):
        tester = DataFormat()
        for data in response.json()['obj']['list']:

            item = GetData().data_get(response)
            item['title_name'] = data['title']
            item['title_date'] = data['issueDate']
            item[
                'title_url'] = f"https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/id={data['id']}/rfqMethod=RAQ/orgCode=UH0940/statusFlag=0"

            try:
                deliveryAddress = data['deliveryAddress']
            except KeyError:
                deliveryAddress = ""

            try:
                materialName = data['materialName']
            except KeyError:
                materialName = ""

            data_dict = {
                "issueDate": data['issueDate'],
                "title": data['title'],
                "issueUsername": data['issueUsername'],
                "materialName": materialName,
                "deliveryAddress": deliveryAddress,
            }
            name_dict = {
                "issueDate": "发布日期",
                "title": "标题名称",
                "issueUsername": "发布人",
                "materialName": "项目介绍",
                "deliveryAddress": "公司地点",
            }
            content_html = tester.dictToHtml(data_dict, name_dict)

            item['content_html'] = content_html

            yield item



    def parse_moreListb(self, response, **kwargs):
        tester = DataFormat()
        for data in response.json()['obj']['newsPage']:

            item = GetData().data_get(response)
            item['title_name'] = data['title']
            item['title_date'] = data['issueDate']
            item['title_url'] = f"https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/id={data['id']}/rfqMethod=RAQ/orgCode=UH0940/statusFlag=1"
            # item['title_url'] = f"http://rfq.ouyeelbuy.com/rfqNotice/bidResListInfo?id={data['id']}&appCode=baowu"

            try:
                deliveryAddress = data['deliveryAddress']
            except KeyError:
                deliveryAddress = ""

            try:
                materialName = data['materialName']
            except KeyError:
                materialName = ""


            data_dict = {
                "issueDate": data['issueDate'],
                "title": data['title'],
                "issueUsername": data['issueUsername'],
                "materialName": materialName,
                "deliveryAddress": deliveryAddress,
            }
            name_dict = {
                "issueDate": "发布日期",
                "title": "标题名称",
                "issueUsername": "发布人",
                "materialName": "项目介绍",
                "deliveryAddress": "公司地点",
            }
            content_html = tester.dictToHtml(data_dict, name_dict)

            item['content_html'] = content_html

            yield item



if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])
