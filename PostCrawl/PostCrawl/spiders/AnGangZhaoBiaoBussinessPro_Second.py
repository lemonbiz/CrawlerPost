"""

鞍钢招标有限公司

"""
import re
import time
from copy import deepcopy

import jsonpath
import scrapy
import scrapy_splash


import ujson
from scrapy.http import JsonRequest


class AngangzhaobiaobussinessproSecondSpider(scrapy.Spider):
    name = 'AnGangZhaoBiaoBussinessPro_Second'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/list?purchaseType=1',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/entrust_know/knowledgeSearch?name=%E5%AF%BB%E6%BA%90%E5%85%AC%E5%91%8A',
    ]

    def start_requests(self):
        for i in range(50):
            yield JsonRequest(
                url="https://bid.ansteelscm.com/notice/pjtnotice/getPjtByPurchaseType",
                data={
                    "idProjectCode": "",
                    "bidProjectName": "",
                    "consignorContactPersonName": "",
                    "consignorEnterpriseName": "",
                    "deadline": "",
                    "noticeType": "20",
                    "pageNum": "1",
                    "pageSize": "10",
                    "pmName": "",
                    "publishStartTime": "",
                    "publishTime": "",
                    "purOrgName": "",
                    "purchaseType": "",
                    "qualifyCheckType": "",
                    "startTime": "",
                },
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    'site_id':deepcopy("3973587172")
                }
            )
        for i in range(50):
            yield JsonRequest(
                url="https://bid.ansteelscm.com/notice/repository/queryRepositoryPage",
                data={
                    "messageHeader": "",
                    "messageTimeBegin": "",
                    "messageTimeOver": "",
                    "organization": "",
                    "pageNum": str(i),
                    "pageSize": "10",
                    "placeTheColumn": "寻源公告",
                },
                callback=self.parse_source,
                meta={
                    "site_path_url":deepcopy(self.start_urls[1]),
                    'site_id': deepcopy("EE2CB2A9DA")
                }

            )


    def parse(self, response, **kwargs):

        item = {}
        json_text = ujson.loads(response.text)

        id_list = jsonpath.jsonpath(json_text, '$..billId')

        title_name_list = jsonpath.jsonpath(json_text, '$..title')

        title_date_list = jsonpath.jsonpath(json_text, '$..ts')

        for id1, title_name, title_date in zip(id_list, title_name_list, title_date_list):
            item['title_name'] = title_name
            timeStamp = int(title_date) / 1000
            timeArray = time.localtime(timeStamp)

            item['title_date'] = time.strftime("%Y-%m-%d", timeArray)

            item['title_url'] = 'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_notice/zb_index?id={}&noticeType=5'.format(
                id1)

            item["content_html"] = "请查看原文  有附件 PDF"

            # 将目录地址 传值到管道中
            item['site_path_url'] = response.meta.get('site_path_url')
            # 目录名
            item["site_path_name"] = '首页 > 我的商机'

            item['site_id'] = response.meta.get('site_id')

            yield item

            # title_url="https://bid.ansteelscm.com/notice/pjtnotice/getBidProjectNoticeByBillId?id={}".format(id1)
            # yield scrapy.Request(
            #     url=item['title_url'],
            #     callback=self.parse_detail,
            #     meta={'item': deepcopy(item)},
            # )

    def parse_source(self, response, **kwargs):
        item = {}
        json_text = ujson.loads(response.text)

        id_list = jsonpath.jsonpath(json_text, '$..id')

        title_name_list = jsonpath.jsonpath(json_text, '$..messageHeader')

        title_date_list = jsonpath.jsonpath(json_text, '$..ts')

        for id1, title_name, title_date in zip(id_list, title_name_list, title_date_list):
            item['title_name'] = title_name
            timeStamp = int(title_date) / 1000
            timeArray = time.localtime(timeStamp)

            item['title_date'] = time.strftime("%Y-%m-%d", timeArray)

            item['title_url'] = 'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/bid_evaluationClarify/knowledgeText?id={}'.format(
                id1)

            # 将目录地址 传值到管道中
            item['site_path_url'] = response.meta.get('site_path_url')
            # 目录名
            item["site_path_name"] = '首页 > 寻源公告'

            item['site_id'] = response.meta.get('site_id')

            title_url = "https://bid.ansteelscm.com/notice/repository/queryRepositoryById?id={}".format(id1)
            yield scrapy.Request(
                url=title_url,
                callback=self.parse_detail,
                meta={'item': deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta.get("item")

        try:
            for it in response.json()['data']['cpuRepositoryContents']:
                item['content_html'] = it['messageContent']
        except:
            item['content_html'] = response.json()
        yield item

if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline
    file_name = os.path.basename(sys.argv[0])
    file_name=file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])