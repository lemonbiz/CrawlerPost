from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class XizangonlineinvestproSpider(scrapy.Spider):
    name = 'XiZangOnlineInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://tzxm.drc.xizang.gov.cn:8008/report/publicInfo']

    def start_requests(self):
        for i in range(1,10):
            yield scrapy.Request(
                url=f"https://tzxm.drc.xizang.gov.cn:8008/report/publicInfo/publicationResults?pages={i}&rows=10&search=",
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    "site_path_name": deepcopy("首页 公示信息 办理结果公示"),
                    "site_id": deepcopy("286C570C3E"),
                },
            )

    def parse(self, response):
        tester = DataFormat()
        for data in response.json()['data']['data']:

            item = GetData().data_get(response)
            item['title_name'] = data['applyProjectName']
            item['title_url'] = f"https://tzxm.drc.xizang.gov.cn:8008/report/publicInfo/{data['dealCode']}"
            item['title_date'] = data['applyTime']

            content_html = tester.dictToHtml(data)

            item['content_html'] = content_html
            yield item



    def parse_detail(self, response):
        item = response.meta['item']

        item['content_html'] = response.css(".run-piece-main.fn-clear").get()

        yield item


if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])