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
    start_urls = ['http://nmg.tzxm.gov.cn/tzsp/projectHandlePublicity.jspx']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[0]),
                    "site_path_name": copy.deepcopy("首页>项目办理结果公示"),
                    "site_id": copy.deepcopy("D6299B0755"),
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

