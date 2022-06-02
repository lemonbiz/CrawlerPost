import json
import time
from copy import deepcopy
import jsonpath
import scrapy
import ujson
from scrapy.http import JsonRequest

from PostCrawl.utils.data_get import GetData


class AngangzhaobiaobussinessproSpider(scrapy.Spider):
    name = 'AnGangZhaoBiaoBussinessPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=4&noticeType=22',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=3&noticeType=22',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=2&noticeType=22',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=1&noticeType=22',
    ]

    def start_requests(self):
        url = "https://bid.ansteelscm.com/notice/pjtnotice/getPjtByPurchaseType"
        yield from self.handle_request(url, 22, 4, site_path_url=self.start_urls[0], site_id="F55375812B",site_path_name="设备备件>中标公告>公示")
        yield from self.handle_request(url, 22, 3, site_path_url=self.start_urls[1], site_id="7F83D8D1E8",site_path_name="服务>中标公告>公示")
        yield from self.handle_request(url, 22, 2, site_path_url=self.start_urls[2], site_id="63461F1DA6",site_path_name="原燃材料>中标公告>公示")
        yield from self.handle_request(url, 22, 1, site_path_url=self.start_urls[3], site_id="87E2984A5E",site_path_name="工程>中标公告>公示")

    def handle_request(self, url, noticeType, purchaseType, site_path_url,site_path_name, site_id):
        for i in range(30):
            yield JsonRequest(
                url=url,
                data={
                    "title": "",
                    "noticeType": str(noticeType),
                    "purchaseType": str(purchaseType),
                    "pageNum": str(i),
                    "pageSize": "10"
                },
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(site_path_url),
                    "site_id": deepcopy(site_id),
                    'site_path_name':deepcopy(site_path_name)
                },
                dont_filter=True,
            )

    gd = GetData()

    def parse(self, response, **kwargs):
        item = {}

        json_text=response.json()
        print(json_text)
        item=self.gd.data_get(response)
        for data in json_text['data']['list']:
            item['title_name'] = data['title']
            timeStamp = int(data['publishTime']) / 1000
            timeArray = time.localtime(timeStamp)
            item['title_date'] = time.strftime("%Y-%m-%d", timeArray)
            # 将目录地址 传值到管道中
            item['title_url'] = 'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_notice/index?id={}'.format(
                        data['id'])

            title_url = "https://bid.ansteelscm.com/notice/pjtnotice/getPjtNoticeById?id={}".format(data['id'])
            yield JsonRequest(
                        url=title_url,
                        callback=self.parse_detail,
                        meta={'item': deepcopy(item)},
                dont_filter=True,
                    )

    def parse_detail(self, response):
        item = response.meta['item']

        content_html = json.loads(response.text)
        try:
            item['content_html'] = jsonpath.jsonpath(content_html, '$..noticeUrl')[0]
        except:
            item['content_html'] = content_html
        yield item


    #     id_list = jsonpath.jsonpath(json_text, '$..id')
    #     id2_list = jsonpath.jsonpath(json_text, '$..billId')
    #     title_name_list = jsonpath.jsonpath(json_text, '$..title')
    #     title_date_list = jsonpath.jsonpath(json_text, '$..ts')
    #
    #     for id1, id2, title_name, title_date in zip(id_list, id2_list, title_name_list, title_date_list):
    #         item['title_name'] = title_name
    #         timeStamp = int(title_date) / 1000
    #         timeArray = time.localtime(timeStamp)
    #         item['title_date'] = time.strftime("%Y-%m-%d", timeArray)
    #         # 将目录地址 传值到管道中
    #         item['site_path_url'] = response.meta.get('site_path_url')
    #         # 目录名
    #         item["site_path_name"] = '首页 > 中标公告/公示'
    #
    #         item['site_id'] = response.meta.get('site_id')
    #
    #         item['title_url'] = 'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_notice/index?id={}'.format(
    #             id1)
    #         title_url = "https://bid.ansteelscm.com/notice/pjtnotice/getPjtNoticeById?id={}".format(id1)
    #
    #         yield JsonRequest(
    #             url=title_url,
    #             callback=self.parse_detail,
    #             meta={'item': deepcopy(item)},
    #         )
    #



if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()
