"""
内蒙古自治区投资项目在线审批监管平台
拟在建项目


"""
import copy
import re
import time
from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData


class NeimengguinvestproSpider(scrapy.Spider):
    name = 'NeiMengGuInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://nmg.tzxm.gov.cn/tzsp/projectHandlePublicity.jspx',
                  'http://nmg.tzxm.gov.cn/indexlink/xxgk.jspx?shareaId=150000&sareaId=150100',

                  ]

    def start_requests(self):
        # for url in self.start_urls:
        #     yield scrapy.Request(
        #         url=url,
        #         callback=self.parse,
        #         meta={
        #             "site_path_url": copy.deepcopy(self.start_urls[0]),
        #             "site_path_name": copy.deepcopy("首页>项目办理结果公示"),
        #             "site_id": copy.deepcopy("D6299B0755"),
        #         }
        #     )

        # for url in [f'http://nmg.tzxm.gov.cn/indexlink/info/beforeApprove.jspx?pageNo={i}&areaid=150000&searchText=&deptId='for i in range(1,6)]:
        # for url in ['http://nmg.tzxm.gov.cn/indexlink/info/beforeApprove.jspx?pageNo=1&areaid=150000&searchText=&deptId=']:
        #     yield scrapy.Request(
        #         url=url,
        #         callback=self.parse_xxgk,
        #         meta={
        #             "site_path_url": copy.deepcopy(self.start_urls[1]),
        #             "site_path_name": copy.deepcopy("首页>投资项目批前公示&投资项目批前公示"),
        #             "site_id": copy.deepcopy("C7C8D7E1B6"),
        #         }
        #     )

        # for url in [f'http://nmg.tzxm.gov.cn/indexlink/info/afterApprove.jspx?pageNo={i}&areaid=150000&searchText=&deptId=&start=&end='for i in range(1,118)]:
        for url in ['http://nmg.tzxm.gov.cn/indexlink/info/afterApprove.jspx?pageNo=1&areaid=150000&searchText=&deptId=&start=&end=']:
            yield scrapy.Request(
                url=url,
                callback=self.parse_xxgk_1,
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[1]),
                    "site_path_name": copy.deepcopy("首页>投资项目批前公示&投资项目批前公示"),
                    "site_id": copy.deepcopy("C7C8D7E1B6"),
                }
            )

    def parse(self, response,**kwargs):

        url_list =response.xpath('/html/body/div/div[1]/div/div[2]/div[2]/div/table//tr/td[1]/a')
        title_list = response.xpath('/html/body/div/div[1]/div/div[2]/div[2]/div/table//tr/td[2]')
        for url,name in zip(url_list,title_list):
            item = GetData().data_get(response)
            item["title_url"] ='http://nmg.tzxm.gov.cn/' + str(url.xpath('./@href').extract_first())
            item["title_name"] = name.xpath('./text()').extract_first()


            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item':deepcopy(item)}
            )

        next_url ='http://nmg.tzxm.gov.cn/'+response.xpath('//div[@class="fanye"]/p/a[4]/@href').extract_first()

        if next_url is not None:
            yield scrapy.Request(
                url = next_url,
                callback=self.parse,
                headers={
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cache-Control': 'no-cache',
                  'Connection': 'keep-alive',
                  'Host': 'nmg.tzxm.gov.cn',
                  'Pragma': 'no-cache',
                  'Referer': 'http://nmg.tzxm.gov.cn/tzsp/projectHandlePublicity.jspx?projectname=&pageNo=1',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
                },
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[0]),
                    "site_path_name": copy.deepcopy("首页>项目办理结果公示"),
                    "site_id": copy.deepcopy("D6299B0755"),
                }
            )
    # 详情页解析
    def parse_detail(self,response):
        item=response.meta['item']
        item['content_html'] = response.body.decode("utf-8")
        try:
            item["title_date"]=re.findall("(\d{4}-\d{2}-\d{2})",str(item['content_html']))[0]
        except IndexError:
            print("网址时间错误 默认当前时间")
            item["title_date"] = time.strftime('%Y-%m-%d %H:%M:%S')
        yield item

    def parse_xxgk(self,response):
        for li in response.css("#table1 tr"):
            item = GetData().data_get(response)
            item["title_url"] = 'http://nmg.tzxm.gov.cn' + str(li.css('td a::attr(href)').get())
            item["title_name"] = li.css('td a::text').get()
            title_date:str = li.css('td:nth-child(4)::text').get()
            if title_date is None:
                continue
            item["title_date"] = title_date.replace("\r\n","")
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail_xxgk,
                meta={'item': deepcopy(item)}
            )

    def parse_detail_xxgk(self,response):
        item=response.meta['item']
        item['content_html'] = response.css(".block_content.bmgk_pad").get()
        yield item

    def parse_xxgk_1(self,response):
        for li in response.css("#table1 tr"):
            item = GetData().data_get(response)
            item["title_url"] = 'http://nmg.tzxm.gov.cn' + str(li.css('td:nth-child(1) a::attr(href)').get())
            item["title_name"] = li.css('td:nth-child(5)::text').get()
            title_date:str = li.css('td:nth-child(5)::text').get()
            if title_date is None:
                continue
            item["title_date"] = title_date
            item['content_html'] = "<html><body><div>请查看原文链接</div></body></html>"

            yield item
