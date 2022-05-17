"""

全国投资项目在线审批监管平台-山东省

"""
import copy
import datetime
import json
import time

import jsonpath
import scrapy

from PostCrawl.utils.data_get import GetData

gd = GetData()


class ShandongprovincebiddingsupervisionproSpider(scrapy.Spider):
    name = 'ShanDongProvinceBiddingSupervisionPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://221.214.94.51:8081/icity/ipro/projectlist']

    def start_requests(self):
        yield scrapy.Request(
            method="POST",
            url='http://221.214.94.51:8081/icity/api-v2/app.icity.ipro.IproCmd/getSPListByPage?s=c117031650417065984&t=3682_c01111_{}'.format(
                int(time.time() * 1000)),
            body=json.dumps(
                {
                    "contractor": "",
                    "page": "1",
                    "projectcode": "",
                    "projectname": "",
                    "projecttype": "",
                    "rows": "100",
                }
            ),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse,
            meta={
                "site_path_url": copy.deepcopy(self.start_urls[0]),
                "site_path_name": copy.deepcopy("审批事项公示信息>（ 赋码项目列表 & 审批事项公示信息）"),
                "site_id": copy.deepcopy("E4CBE66D3A"),
            },
        )

    def parse(self, response, **kwargs):
        for data in response.json()['data']:
            item = gd.data_get(response)
            item["title_name"] = data['PROJECT_NAME']

            item['title_url'] = 'http://221.214.94.51:8081/icity/ipro/fmxmgs?sqlid={}&bsnum={}'.format(data['SEQ_ID'],
                                                                                                       data['BSNUM'])
            title_date: str = data['PROJECT_CODE']
            date: str = title_date.split('-')[0]
            date1 = date[0:2]
            date2 = date[2:4]
            item["title_date"] = "20" + date1 + "-" + date2 + "-01"
            item['site_path_url'] = self.start_urls[0]
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item['content_html'] = response.css("#w-d-x-1").get()
        yield item


if __name__ == '__main__':
    gd.crawler_run()
