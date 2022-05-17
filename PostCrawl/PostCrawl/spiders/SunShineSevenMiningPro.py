"""

阳光七采·兵纷招采—中国兵器电子招标投标交易平台

"""
import copy
import datetime
import operator
import re


import scrapy

from PostCrawl.utils.data_get import GetData


class SunshinesevenminingproSpider(scrapy.Spider):
    name = 'SunShineSevenMiningPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://bid.norincogroup-ebuy.com/retrieve.do']

    def start_requests(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=5)
        ggyxq_time1 = now + delta
        ggyxq_time = ggyxq_time1.strftime('%Y-%m-%d 00:00:00')
        print(ggyxq_time)
        yield scrapy.FormRequest(
            url="https://bid.norincogroup-ebuy.com/retrieve.do",
            formdata={'fl': '',
                      'hy': '',
                      'dq': '',
                      'es': '1',
                      'keyFlag': '',
                      'packtype': '',
                      'packtypeCode': '',
                      'packtypeValue': '',
                      'packtypeCodeValue': '',
                      'typflag': '1',
                      'fbdays': '0',
                      'esly': '',
                      'validityPeriodFlag': '',
                      'flag1': '1',
                      'orderby': '1',
                      'keyConValue': '',
                      'keyCon': '',
                      'fbDateStart': '',
                      'fbDateEnd': '',
                      'radio': 'on',
                      'ggyxq_time': str(ggyxq_time),
                      'pageNumber': "1",
                      'pageSize': '50',
                      'sortColumns': 'undefined'},
            callback=self.parse,
            headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
                "Referer": "https://bid.norincogroup-ebuy.com/retrieve.do",
            },
            meta={
                "site_path_url": copy.deepcopy(self.start_urls[0]),
                "site_path_name": copy.deepcopy("招标信息"),
                "site_id": copy.deepcopy("B2FEA850DA"),
            },
            dont_filter=True,
            )

    # def start_requests(self):
    #     now = datetime.datetime.now()
    #     delta = datetime.timedelta(days=5)
    #     ggyxq_time1 = now + delta
    #     ggyxq_time = ggyxq_time1.strftime('%Y-%m-%d 00:00:00')
    #     for i in range(1, 700):
    #         yield scrapy.FormRequest(
    #             url="https://bid.norincogroup-ebuy.com/retrieve.do",
    #             formdata={'fl': '',
    #                       'hy': '',
    #                       'dq': '',
    #                       'es': '1',
    #                       'keyFlag': '',
    #                       'packtype': '',
    #                       'packtypeCode': '',
    #                       'packtypeValue': '',
    #                       'packtypeCodeValue': '',
    #                       'typflag': '1',
    #                       'fbdays': '0',
    #                       'esly': '',
    #                       'validityPeriodFlag': '',
    #                       'flag1': '1',
    #                       'orderby': '1',
    #                       'keyConValue': '',
    #                       'keyCon': '',
    #                       'fbDateStart': '',
    #                       'fbDateEnd': '',
    #                       'radio': 'on',
    #                       'ggyxq_time': str(ggyxq_time),
    #                       'pageNumber': str(i),
    #                       'pageSize': '10',
    #                       'sortColumns': 'undefined'},
    #             callback=self.parse,
    #             headers={
    #                 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    #                 "Referer": "https://bid.norincogroup-ebuy.com/retrieve.do",
    #                 "Cookie": "UM_distinctid=17f919fc6784ee-0ccbde6c340d27-9771539-1fa400-17f919fc679131e; JSESSIONID=E95B4751B6D762F542558715288BD939.node1; CNZZDATA1273116668=1237850760-1647409725-%7C1647912735; Hm_lvt_5ab6a469ba9c2d97f839c81cad6c2b72=1647415643,1647915196; Hm_lpvt_5ab6a469ba9c2d97f839c81cad6c2b72=1647917625",
    #             }
    #
    #         )

    def parse(self, response, **kwargs):
        gd = GetData()
        for div in response.xpath("//div[@class='zbztbn_bgbox']/div[@class='item']"):
            item = gd.data_get(response)
            item["title_name"] = div.xpath(".//a[@class='sldivTitle']/@title").extract_first()
            item["title_url"] = div.xpath(".//a[@class='sldivTitle']/@href").extract_first()
            title_date: str = div.xpath('.//span[@class="date"]/text()[1]').extract_first()
            item["title_date"] = title_date.split(":")[1]



    #         # title_url=f"https://bidfile.norincogroup-ebuy.com/bdfileservice//upfile2009/bdsnapshot/zbgg/{url_code}/{url_code}.html"
    #
            yield scrapy.Request(
                url=item["title_url"],
                callback=self.parse_detail,
                meta={
                    "item": copy.deepcopy(item)
                },
            )

    def parse_detail(self, response):
        item = response.meta.get("item")

        item["content_html"] = response.css("html body").get()

        yield item

if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline
    file_name = os.path.basename(sys.argv[0])
    file_name=file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])