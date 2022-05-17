"""

河北省生态环境信息中心

"""

import copy
import re

import scrapy


class HebeiprovinceecologyenvironmentproSpider(scrapy.Spider):
    name = 'HebeiProvinceEcologyEnvironmentPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://110.249.223.65:8070/spmh/searchallnipizhun.action?cpage=1&gsid=1&xmmc=&jsdw=&deptid=1',
        'http://110.249.223.65:8070/spmh/searchallnipizhun2.action?deptid=1&gsid=5',
        'http://110.249.223.65:8070/spmh/searchallnipizhun2.action?deptid=1&gsid=6',
        'http://110.249.223.65:8070/spmh/searchallspxmgg.action?deptid=1&gsid=2',
        'http://110.249.223.65:8070/spmh/searchalljgys.action?deptid=1&gsid=7',
        'http://110.249.223.65:8070/spmh/searchalljgys.action?deptid=1&gsid=8',
        'http://110.249.223.65:8070/spmh/searchalljgys.action?deptid=1&gsid=9',
        'http://110.249.223.65:8070/spmh/searchallspxmgg.action?deptid=1&gsid=10',
    ]

    def start_requests(self):

        url_list_1 = ["http://110.249.223.65:8070/spmh/searchallnipizhun.action?cpage=1&gsid=1&xmmc=&jsdw=&deptid=1"]

        url_list_2 = ["http://110.249.223.65:8070/spmh/searchallnipizhun2.action?cpage=1&gsid=5&xmmc=&jsdw=&deptid=1"]

        url_list_3 = ["http://110.249.223.65:8070/spmh/searchallnipizhun2.action?cpage=1&gsid=6&xmmc=&jsdw=&deptid=1"]

        url_list_4 = ["http://110.249.223.65:8070/spmh/searchallspxmgg.action?cpage=1&gsid=2&xmmc=&deptid=1"]
        url_list_5 = ["http://110.249.223.65:8070/spmh/searchalljgys.action?cpage=1&gsid=7&xmmc=&jsdw=&deptid=1"]
        url_list_6 = ["http://110.249.223.65:8070/spmh/searchalljgys.action?cpage=1&gsid=8&xmmc=&jsdw=&deptid=1"]
        url_list_7 = ["http://110.249.223.65:8070/spmh/searchalljgys.action?cpage=1&gsid=9&xmmc=&jsdw=&deptid=1"]

        url_list_8 = ["http://110.249.223.65:8070/spmh/searchallspxmgg.action?cpage=1&gsid=10&xmmc=&deptid=1"]

        yield from self.handle_request(url_list_1, self.start_urls[0])
        yield from self.handle_request(url_list_2, self.start_urls[1])
        yield from self.handle_request(url_list_3, self.start_urls[2])
        yield from self.handle_request(url_list_4, self.start_urls[3])
        yield from self.handle_request(url_list_5, self.start_urls[4])
        yield from self.handle_request(url_list_6, self.start_urls[5])
        yield from self.handle_request(url_list_7, self.start_urls[6])
        yield from self.handle_request(url_list_8, self.start_urls[7])

    def handle_request(self, url_list_1, site_path_url):
        for url in url_list_1:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy(site_path_url),
                }
            )

    def parse(self, response, **kwargs):
        item = {}
        for tr in response.css("#table-ex tr"):
            item['title_name'] = tr.css("td a::text").get()
            title_url: str = tr.css("td a::attr(href)").get()
            title_date: str = tr.css("td:nth-child(3)::text").get()
            title_date: str = re.sub(r'\r\n', '', title_date)
            title_date: str = re.sub(r' ', '', title_date)
            item['title_date'] = re.sub(r'\t', '', title_date)

            item['title_url'] = "http://110.249.223.65:8070/spmh/" + str(title_url)


            item['site_path_name'] = "公示公告>>建设项目环境影响评价文件审批>（环境影响评价文件受理情况公示 & 环评项目拟批准公示 & 环评项目拟不予批准公示 & 环评项目审批决定公告）建设项目竣工环境保护验收（固废） 验收项目（受理情况公示 & 验收项目拟批准公示 & 验收项目拟不予批准公示 & 验收项目审批决定公告）"
            item['site_id'] = "ED81D90050"
            # item['site_path_url'] = response.meta.get("site_path_url")
            item['site_path_url'] = "http://110.249.223.65:8070/spmh/gonggao/gonggaoindex.jsp?deptid=1"

            yield scrapy.Request(
                url=item["title_url"],
                callback=self.parse_detail,
                meta={
                    "item": copy.deepcopy(item)
                }
            )

    def parse_detail(self, response):
        item = response.meta.get("item")
        item['content_html'] = response.css("body > div > div:nth-child(4)").get()

        yield item


if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline
    file_name = os.path.basename(sys.argv[0])
    file_name=file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])