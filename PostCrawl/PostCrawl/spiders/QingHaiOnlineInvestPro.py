import time
from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData


class QinghaionlineinvestproSpider(scrapy.Spider):
    name = 'QingHaiOnlineInvestPro'
    # allowed_domains = ['xx.com']
    start_urls = ['http://www.qhtzxm.gov.cn/info/toListPage']

    def start_requests(self):
        for i in range(1,500):
            yield scrapy.Request(
                url=f"http://www.qhtzxm.gov.cn/publicResults/getPublicResults"
                    f"?pageNumber={i}"
                    f"&pageSize=10"
                    f"&dealCode="
                    f"&projectName="
                    f"&taskName="
                    f"&curTab=0"
                    f"&deptCode="
                    f"&impStatus=",

                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    "site_path_name": deepcopy("首页>信息公开>办件评价公示"),
                    "site_id": deepcopy("DB82A01348"),
                }
            )

    def parse(self, response):
        for data in response.json()['resultData']['results']['list']:
            print(data)
            item = GetData().data_get(response)
            item['title_name'] = data['project_name']
            item[
                'title_url'] = f"http://www.qhtzxm.gov.cn/publicResults/details?projectUuid={data['projectUuid']}&dealCode={data['deal_code']}"
            item['title_date'] = data['update_time']

            if item['title_date'] is None:
                item['title_date'] = time.strftime('%Y-%m-%d %H:%M:%S')

            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )

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
