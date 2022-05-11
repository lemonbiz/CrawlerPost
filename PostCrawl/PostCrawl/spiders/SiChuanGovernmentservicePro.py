"""

全国投资项目在线审批监管平台-四川省

"""
from copy import deepcopy

import scrapy
import requests
from PostCrawl.utils.data_get import GetData


class SichuangovernmentserviceproSpider(scrapy.Spider):
    name = 'SiChuanGovernmentservicePro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://sc.tzxm.gov.cn/showinformation']

    def start_requests(self):
        url = "http://sc.tzxm.gov.cn/showinformation"

        yield scrapy.FormRequest(
            url=url,
            formdata={
                "pageNo": "1",
                "tabType": "",
                "tinsBusinessinfo.projectname": "",
                "ywstatus_value": "",
                "starttime": "",
                "endtime": "",
            },
            callback=self.parse,
            meta={
                "site_path_url": deepcopy(self.start_urls[0]),
                "site_path_name": deepcopy("信息公开>投资项目办理结果公示"),
                "site_id": deepcopy("7829271EA0"),
            },
            dont_filter=True,
        )

        # for i in range(1,193):
        #     yield scrapy.FormRequest(
        #         url=url,
        #         formdata={
        #             "pageNo": str(i),
        #             "tabType": "",
        #             "tinsBusinessinfo.projectname": "",
        #             "ywstatus_value": "",
        #             "starttime": "",
        #             "endtime": "",
        #         },
        #         callback=self.parse,
        #         meta={
        #             "site_path_url": deepcopy(self.start_urls[0]),
        #             "site_path_name": deepcopy("信息公开>投资项目办理结果公示"),
        #             "site_id": deepcopy("7829271EA0"),
        #         },
        #     )

    def parse(self, response, **kwargs):
        item = GetData().data_get(response)

        for div in response.xpath('//*[@id="dvRight1"]/table//tr'):

            # 调用item
            item["title_name"] = div.xpath('./td[2]/text()').extract_first()
            title_url: str = div.xpath(".//a/@href").extract_first()

            if title_url is None:
                continue
            item["title_url"] = "http://sc.tzxm.gov.cn" + str(title_url)
            title_date: str = div.xpath('./td[6]/text()').extract_first()
            item["title_date"] = str(title_date).replace("\n", "")
            item['site_path_url'] = self.start_urls[0]

            html = requests.get(item['title_url']).text

            res = scrapy.Selector(text=html)

            item["content_html"] = res.xpath("//*[@class='t4_xm_table t4_bszn2_table']").get()

            yield item
