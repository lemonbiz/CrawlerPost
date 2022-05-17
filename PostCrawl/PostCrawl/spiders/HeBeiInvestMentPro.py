'''
河北省投资项目在线审批监管平台
'''
import copy
import re

import scrapy

from PostCrawl.utils.data_get import GetData


class HebeiinvestmentproSpider(scrapy.Spider):
    name = 'HeBeiInvestMentPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://tzxm.hbzwfw.gov.cn/sbglweb/channelContentListpt',
        'http://tzxm.hbzwfw.gov.cn/sbglweb/channelContentList',
    ]

    def start_requests(self):
        for i in range(1):
            channelID = '402881da5215a653015215be1eea033f'
            yield from self.handle_request(self.parse_pt,channelID, i, self.start_urls[0], site_id="6C0F5C9316",site_path_name="首页 > 政策法规")

        for i in range(1):
            channelID = 'A8FE5F40FFFFFFFFEB4F9270FFFFFFBF'
            yield from self.handle_request(self.parse,channelID, i, self.start_urls[1], site_id="9266C683CF",site_path_name="首页 > 平台动态")



    def handle_request(self,callback, channelID, i, site_path_url, site_id,site_path_name):
        yield scrapy.FormRequest(
            url=site_path_url,
            formdata={
                'channelID': channelID,
                'query': '请输入关键字',
                'rows': '10',
                'page': str(i + 1),
            },
            callback=callback,
            meta={
                "site_path_url": copy.deepcopy(site_path_url),
                "site_id": copy.deepcopy(site_id),
                "site_path_name": copy.deepcopy(site_path_name),
            }
        )


    def parse_pt(self,response):
        for li in response.css(".ejlistwrap ul li"):
            item = GetData().data_get(response)

            title_url:str = li.css("a::attr(href)").get()
            item['title_url'] = "http://tzxm.hbzwfw.gov.cn/sbglweb/"+title_url
            item['title_name'] = li.css("a::text").get()
            item['title_date'] = li.css("span::text").get()

            content_id = title_url.split("contentID=")[1]

            true_url =f"http://tzxm.hbzwfw.gov.cn/sbglweb/ptdtInfoN?contentID={content_id}"
            yield scrapy.Request(
                url=true_url,
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)},
            )

    def parse(self, response, **kwargs):

        for li in response.css(".ejlistwrap ul li"):
            item = GetData().data_get(response)

            title_url: str = li.css("a::attr(href)").get()
            item['title_url'] = "http://tzxm.hbzwfw.gov.cn/sbglweb/" + title_url
            item['title_name'] = li.css("a::text").get()
            item['title_date'] = li.css("span::text").get()

            content_id = title_url.split("contentID=")[1]

            true_url = f"http://tzxm.hbzwfw.gov.cn/sbglweb/ptdtInfoN?contentID={content_id}"
            yield scrapy.Request(
                url=true_url,
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)},
            )
    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.text
        yield item


if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])

