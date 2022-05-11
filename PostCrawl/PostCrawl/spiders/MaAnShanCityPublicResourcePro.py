"""
安徽省招标投标信息网
"""
import copy
import time
from copy import deepcopy

import scrapy

import re


class MaanshancitypublicresourceproSpider(scrapy.Spider):
    name = 'MaAnShanCityPublicResourcePro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://zbcg.mas.gov.cn/fwdt/002005/002005001/tradelist.html',
        'http://zbcg.mas.gov.cn/fwdt/002005/002005002/tradelist.html',
        'http://zbcg.mas.gov.cn/fwdt/002005/002005003/tradelist.html',
        'http://zbcg.mas.gov.cn/fwdt/002005/002005004/tradelist.html',
    ]

    def start_requests(self):
        url_list_1 = ['http://zbcg.mas.gov.cn/fwdt/002005/002005001/tradelist.html']
        url_list_2 = ['http://zbcg.mas.gov.cn/fwdt/002005/002005002/tradelist.html']
        url_list_3 = ['http://zbcg.mas.gov.cn/fwdt/002005/002005003/tradelist.html']
        url_list_4 = ['http://zbcg.mas.gov.cn/fwdt/002005/002005004/tradelist.html']

        # url_list_1=["http://zbcg.mas.gov.cn/fwdt/002005/002005001/{}.html".format(i)for i in range(2,1000)]
        # url_list_2=["http://zbcg.mas.gov.cn/fwdt/002005/002005002/{}.html".format(i)for i in range(2,1000)]
        # url_list_3=["http://zbcg.mas.gov.cn/fwdt/002005/002005003/{}.html".format(i)for i in range(2,1000)]
        # url_list_4=["http://zbcg.mas.gov.cn/fwdt/002005/002005004/{}.html".format(i)for i in range(2,5)]

        yield from self.handle_request(url_list_1, self.start_urls[0], site_path_name="首页>服务大厅>交易信息>建设工程",
                                       site_id="87136AAE78")
        yield from self.handle_request(url_list_2, self.start_urls[1], site_path_name="关键词“矿”搜索", site_id="40FDD3318B")
        yield from self.handle_request(url_list_3, self.start_urls[2], site_path_name="首页>服务大厅>交易信息>土地（矿业权",
                                       site_id="7F9CBC2659")
        yield from self.handle_request(url_list_4, self.start_urls[3], site_path_name="首页>服务大厅>交易信息>产权交易",
                                       site_id="3D8F725B81")

    # def start_requests(self):
    #     url_list_1=["http://zbcg.mas.gov.cn/fwdt/002005/002005001/{}.html".format(i)for i in range(2,1000)]
    #     url_list_2=["http://zbcg.mas.gov.cn/fwdt/002005/002005002/{}.html".format(i)for i in range(2,1000)]
    #     url_list_3=["http://zbcg.mas.gov.cn/fwdt/002005/002005003/{}.html".format(i)for i in range(2,1000)]
    #     url_list_4=["http://zbcg.mas.gov.cn/fwdt/002005/002005004/{}.html".format(i)for i in range(2,5)]
    #
    #     yield from self.handle_request(url_list_1,self.start_urls[0])
    #     yield from self.handle_request(url_list_2,self.start_urls[1])
    #     yield from self.handle_request(url_list_3,self.start_urls[2])
    #     yield from self.handle_request(url_list_4,self.start_urls[3])

    def handle_request(self, url_list, site_path_url, site_path_name, site_id):
        for url in url_list:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(site_path_url),
                    "site_path_name": deepcopy(site_path_name),
                    "site_id": deepcopy(site_id),
                },
                dont_filter=True,
            )

    def parse(self, response, **kwargs):
        item = {}
        title_list = response.xpath('/html/body/div[2]/div[2]/div[2]/div[3]/ul/li')
        for li in title_list:
            item["title_url"] = "http://zbcg.mas.gov.cn/" + li.xpath('./div/a/@href').extract_first()
            item["title_name"] = li.xpath('./div/a/text()').extract_first()
            item["title_date"] = li.xpath('./span/text()').extract_first()
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)}
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item['content_html'] = response.xpath('/html/body/div[2]/div/div[2]').extract_first()

        yield item
