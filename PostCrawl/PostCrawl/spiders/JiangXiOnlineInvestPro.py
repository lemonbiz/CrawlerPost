"""

江西省投资项目在线审批监管平台

"""
from copy import deepcopy

import scrapy
import time

from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class JiangxionlineinvestproSpider(scrapy.Spider):
    name = 'JiangXiOnlineInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://tzxm.jxzwfww.gov.cn/icity/ipro/open/publicity']

    def start_requests(self):
        for i in range(1,500):
            yield scrapy.FormRequest(
                url=f"http://tzxm.jxzwfww.gov.cn/icity/api-v2/jxtzxm.app.icity.ipro.IproCmd/getDisplayListByPage?s=c566831652436749556&t=6219_c75166_{int(time.time()*1000)}&o=657111",
                formdata={
                    "page": str(i),
                    "rows": "10",
                    "type": "0",
                    "projectName": "",
                    "projectCode": ""
                },
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    "site_path_name": deepcopy("首页>公示信息>（备案信息公示&项目赋码情况公示）"),
                    "site_id": deepcopy("88824A29aq"),
                },
            )

    def parse(self, response):
        tester = DataFormat()
        for data in response.json()['data']:
            print(data)
            item = GetData().data_get(response)
            item['title_name'] = data['columns']['APPLY_SUBJECT']
            item['title_url'] = f"http://tzxm.jxzwfww.gov.cn/icity/ipro/open/publicity/{data['columns']['SEQ_ID']}"
            item['title_date'] = data['columns']['FINISH_TIME']

            content_html = tester.dictToHtml(data['columns'])

            item['content_html'] = content_html
            yield item



if __name__ == '__main__':


    import sys
    import os
    from scrapy import cmdline


    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])