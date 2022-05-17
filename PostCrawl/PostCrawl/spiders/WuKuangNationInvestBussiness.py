

import scrapy


class WukuangnationinvestbussinessSpider(scrapy.Spider):
    name = 'WuKuangNationInvestBussiness'
    # allowed_domains = ['xx.com']
    start_urls = ['http://www.ewkzb.com/index//portal/project_pro_init.htm']

    def start_requests(self):
        url = "http://www.ewkzb.com/index/portal/project_pro_list.htm"

        yield scrapy.FormRequest(
            url=url,
            formdata={
                "pgn": "2",
                "title": "",
                "bidName": "",
                "procureType": "",
                "startTime": "",
                "endTime": "",
                "bidSummary": "",
                "sysName": "",
                "bidCode": "",
            },
            callback=self.parse
        )

    def parse(self, response):
        print(response)

if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline
    file_name = os.path.basename(sys.argv[0])
    file_name=file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])