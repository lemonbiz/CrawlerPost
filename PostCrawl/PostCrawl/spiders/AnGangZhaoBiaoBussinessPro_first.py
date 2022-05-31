"""

鞍钢招标有限公司

"""
import time
from copy import deepcopy
import jsonpath
import scrapy
import ujson
from scrapy.http import JsonRequest

from PostCrawl.utils.data_get import GetData


class AngangzhaobiaobussinessproFirstSpider(scrapy.Spider):
    name = 'AnGangZhaoBiaoBussinessPro_first'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=1&noticeType=23',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=2&noticeType=23',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=3&noticeType=23',
        'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/supply_workbench/listmore?purchaseType=4&noticeType=23',
    ]

    def start_requests(self):
        url = "https://bid.ansteelscm.com/notice/pjtnotice/getPjtByPurchaseType"

        yield from self.handle_request(url, 23, 1, site_path_url=self.start_urls[0], site_id="95A893E98B")
        yield from self.handle_request(url, 23, 2, site_path_url=self.start_urls[1], site_id="E5CEFF2535")
        yield from self.handle_request(url, 23, 3, site_path_url=self.start_urls[2], site_id="937ED2CC43")
        yield from self.handle_request(url, 23, 4, site_path_url=self.start_urls[3], site_id="5CE59ACB7A")

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

        for it in json_text['data']['list']:
            # print(it)
            timeStamp = it['ts'] / 1000
            timeArray = time.localtime(timeStamp)
            id1 = it['id']
            id2 = it['billId']
            title_url = f"https://bid.ansteelscm.com/project/changeNotice/query?id={id2}"

            item['title_name'] = it['title']
            item['title_date'] = time.strftime("%Y-%m-%d", timeArray)
            # 将目录地址 传值到管道中
            item['site_path_url'] = response.meta.get('site_path_url')
            # 目录名
            item["site_path_name"] = '首页 > 变更公告'

            item['site_id'] = response.meta.get('site_id')

            item[
                'title_url'] = 'https://bid.ansteelscm.com/cpu-angang-bid-fe/portalcas.html#/pages/bid_notice/webportalviewnotice?id={}&from=1'.format(
                id2)
            yield scrapy.Request(
                url=title_url,
                callback=self.parse_detail,
                meta={'item': deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta.get("item")
        try:
            item['content_html'] = jsonpath.jsonpath(response.json(), '$..noticeContent')[0]
        except:
            item['content_html'] = response.text
        yield item


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()