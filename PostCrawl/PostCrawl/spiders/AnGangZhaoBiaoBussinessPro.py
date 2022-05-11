import json
import time
from copy import deepcopy
import jsonpath
import scrapy
import ujson
from scrapy.http import JsonRequest


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
        yield from self.handle_request(url, 22, 4, site_path_url=self.start_urls[0], site_id="F55375812B")
        yield from self.handle_request(url, 22, 3, site_path_url=self.start_urls[1], site_id="7F83D8D1E8")
        yield from self.handle_request(url, 22, 2, site_path_url=self.start_urls[2], site_id="63461F1DA6")
        yield from self.handle_request(url, 22, 1, site_path_url=self.start_urls[3], site_id="87E2984A5E")

    def handle_request(self, url, noticeType, purchaseType, site_path_url, site_id):
        yield JsonRequest(
            url=url,
            data={
                "title": "",
                "noticeType": str(noticeType),
                "purchaseType": str(purchaseType),
                "pageNum": "0",
                "pageSize": "50"
            },
            callback=self.parse,
            meta={
                "site_path_url": deepcopy(site_path_url),
                "site_id": deepcopy(site_id)
            }
        )

    def parse(self, response, **kwargs):
        item = {}
        json_text = ujson.loads(response.text)
        id_list = jsonpath.jsonpath(json_text, '$..id')
        id2_list = jsonpath.jsonpath(json_text, '$..billId')
        title_name_list = jsonpath.jsonpath(json_text, '$..title')
        title_date_list = jsonpath.jsonpath(json_text, '$..ts')

        for id1, id2, title_name, title_date in zip(id_list, id2_list, title_name_list, title_date_list):
            item['title_name'] = title_name
            timeStamp = int(title_date) / 1000
            timeArray = time.localtime(timeStamp)
            item['title_date'] = time.strftime("%Y-%m-%d", timeArray)
            # 将目录地址 传值到管道中
            item['site_path_url'] = response.meta.get('site_path_url')
            # 目录名
            item["site_path_name"] = '首页 > 中标公告/公示'

            item['site_id'] = response.meta.get('site_id')

            item['title_url'] = 'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_notice/index?id={}'.format(
                id1)
            title_url = "https://bid.ansteelscm.com/notice/pjtnotice/getPjtNoticeById?id={}".format(id1)

            yield JsonRequest(
                url=title_url,
                callback=self.parse_detail,
                meta={'item': deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']

        content_html = json.loads(response.text)
        try:
            item['content_html'] = jsonpath.jsonpath(content_html, '$..noticeUrl')[0]
        except:
            item['content_html'] = content_html
        yield item


if __name__ == '__main__':
    import os

    os.system(f"scrapy crawl AnGangZhaoBiaoBussinessPro", )
