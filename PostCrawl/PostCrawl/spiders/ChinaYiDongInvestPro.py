import re
from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData


class ChinayidonginvestproSpider(scrapy.Spider):
    name = 'ChinaYiDongInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://b2b.10086.cn/b2b/main/preSupplierManagement.html',
                  ]

    def start_requests(self):

        for i in range(1,2):
            formdata = {
                "page.currentPage": str(i),
                "page.perPageSize": "20",
                "noticeBean.noticeType": "",
                "noticeBean.noticeTypeName": "",
                "noticeBean.companyType": "",
                "noticeBean.companyName": "",
                "noticeBean.title": "",
                "noticeBean.startDate": "",
                "noticeBean.endDate": "",
            }
            yield scrapy.FormRequest(
                url="https://b2b.10086.cn/b2b/main/showSupplier.html",
                callback=self.parse,
                formdata=formdata,
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    "site_path_name": deepcopy("供应商公告"),
                    "site_id": deepcopy("9AEB788756"),
                },
            )


    def parse(self, response):
        for tr in response.css(".zb_result_table tr"):
            item = GetData().data_get(response)
            item['title_name'] = tr.css('a::text').get()

            if item['title_name'] is None:
                continue
            onclick: str = tr.css('tr::attr(onclick)').get()
            title_url: str = re.search("(\d+)", onclick).group(1)
            item['title_url'] = f"https://b2b.10086.cn/b2b/main/viewVendorNoticeContent.html?noticeBean.id={title_url}"
            item['title_date'] = tr.css('td:nth-child(4)::text').get()
            yield scrapy.Request(
                url = item['title_url'],
                callback=self.parse_detail,
                meta={
                    "item":deepcopy(item)
                }
            )

    def parse_detail(self,response):
        item = response.meta['item']

        item['content_html'] = response.css("#tableWrap").get()
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'ChinaYiDongInvestPro'])
