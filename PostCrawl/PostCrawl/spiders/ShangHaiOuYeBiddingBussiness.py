"""

欧冶工业品

"""
import copy

import httpx
import jsonpath
import scrapy
import ujson
from scrapy.http import JsonRequest

from PostCrawl.utils.Mixins import Mixins
from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class ShanghaiouyebiddingbussinessSpider(scrapy.Spider):
    name = 'ShangHaiOuYeBiddingBussiness'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://www.obei.com.cn/obei-web-ec-ego/ego/home/noticeList.html?noticeType=1',
        'https://www.obei.com.cn/obei-web-ec-ego/ego/home/noticeList.html?noticeType=2',

    ]

    def start_requests(self):
        for i in range(1,50):
            yield JsonRequest(
                url="https://www.obei.com.cn/obei-gateway/egogateway/n/ouyeelbuyAdmin/getNotice",
                data={"page": str(i),
                          "rows": 10,
                          "pageFlag": "addSelect",
                          "memo": "obei",
                          "noticeType": "1",
                          "rfqMethod": "",
                          "publicBiddingFlag": "",
                          "ouName": "",
                          "sidx": "issueDate",
                          "sord": "desc"},
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy("https://www.obei.com.cn/obei-web-ec-ego/ego/home/noticeList.html?noticeType=1"),
                    "site_path_name": copy.deepcopy("采购公告"),
                    "site_id": copy.deepcopy("F37358EE03"),
                }
            )
        for i in range(1,50):
            yield JsonRequest(
                url="https://www.obei.com.cn/obei-gateway/egogateway/n/ouyeelbuyAdmin/getNotice",
                data={"page": str(i),
                          "rows": 10,
                          "pageFlag": "addSelect",
                          "memo": "obei",
                          "noticeType": "2",
                          "rfqMethod": "",
                          "publicBiddingFlag": "",
                          "ouName": "",
                          "sidx": "requestEndDate",
                          "sord": "desc"},
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy("https://www.obei.com.cn/obei-web-ec-ego/ego/home/noticeList.html?noticeType=2"),
                    "site_path_name": copy.deepcopy("成交公告"),
                    "site_id": copy.deepcopy("5905E1FEDE"),
                }
            )

    gd = GetData()
    df = DataFormat()
    def parse(self, response, **kwargs):
        item = self.gd.data_get(response)
        for data in response.json()['list']:
            item['title_name'] = data['ouName']+"————"+data['title']
            item['title_date'] = data.get('issueDate')



            item['title_url'] = f"https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/" \
                                f"id={data['id']}/" \
                                f"rfqMethod={data['rfqMethod']}/orgCode={data['uuCode']}/statusFlag={data['publicBiddingFlag']}"

            formdata={"rfqMethod":data['rfqMethod'],"id":data['id'],"page":data['page'],"rows":9999}
            yield JsonRequest(
                url="https://www.obei.com.cn/obei-gateway/ego-rfq-raq/n/transaction/announcementSup",
                callback=self.parse_detail,
                data=formdata,
                meta={
                    "item":copy.deepcopy(item)
                },
                dont_filter=True
                                 )

    def parse_detail(self,response):
        item = response.meta['item']
        item['content_html']=self.df.dictToHtml(response.json()['data'])
        yield item


if __name__ == '__main__':
    GetData().crawler_run()