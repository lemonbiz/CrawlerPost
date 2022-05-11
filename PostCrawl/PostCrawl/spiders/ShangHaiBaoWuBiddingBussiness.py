"""

中国宝武采购专区/欧冶工业品

"""
import copy

import httpx
import jsonpath
import scrapy
import ujson



class ShanghaibaowubiddingbussinessSpider(scrapy.Spider):
    name = 'ShangHaiBaoWuBiddingBussiness'
    # allowed_domains = ['xxx.com']
    start_urls = [
                  'http://baowu.ouyeelbuy.com/baowu-shp/moreListb.html',
                  'http://baowu.ouyeelbuy.com/baowu-shp/moreLista.html',
                  'http://baowu.ouyeelbuy.com/baowu-shp/notice/entrustPublicity.html',
                  ]

    def start_requests(self):
        yield scrapy.FormRequest(
            url="http://baowu.ouyeelbuy.com/baowu-shp/notice/moreEntrustPublicity",
            formdata={
                "title": "",
                "sDate": "",
                "eDate": "",
                "type": "",
                "pageNow": "1",
                "jqMthod": "newsList",
                "ouName": "",
            },
            callback=self.parse,
            meta={
                "site_path_url": copy.deepcopy(self.start_urls[2]),
                "site_path_name": copy.deepcopy("首页>委托公示"),
                "site_id": copy.deepcopy("57586E200E"),
            }
        )
        yield scrapy.FormRequest(
            url="http://baowu.ouyeelbuy.com/baowu-shp/notice/purchaseMore?pageFlag=addSelect&pageSize=20",
            formdata={
                "sDate": "",
                "eDate": "",
                "title": "",
                "ouName": "",
                "rfqMethod": "",
                "cTeam": "",
                "type": "purchase",
                "pageNow": "1",
                "jqMthod": "newsList",
            },
            meta={
                "site_path_url": copy.deepcopy(self.start_urls[0]),
                "site_path_name": copy.deepcopy("中标公告"),
                "site_id": copy.deepcopy("02BE6D076E"),
            },
            callback=self.parse_moreListb
        )

        yield scrapy.FormRequest(
            url="http://baowu.ouyeelbuy.com/baowu-shp/notice/purchaseMore?pageFlag=addSelect&pageSize=20",
            formdata={
                "sDate": "",
                "eDate": "",
                "title": "",
                "ouName": "",
                "rfqMethod": "",
                "cTeam": "",
                "type": "purchase",
                "pageNow": "2",
                "jqMthod": "newsList",
            },
            meta={
                "site_path_url": copy.deepcopy(self.start_urls[1]),
                "site_path_name": copy.deepcopy("采购公告"),
                "site_id": copy.deepcopy("DC245BEA15"),
            },
            callback=self.parse1
        )


    # def start_requests(self):
    #     for i in range(1,5):
    #         yield scrapy.FormRequest(
    #             url="http://baowu.ouyeelbuy.com/baowu-shp/notice/moreEntrustPublicity",
    #             formdata={
    #                 "title": "",
    #                 "sDate": "",
    #                 "eDate": "",
    #                 "type": "",
    #                 "pageNow": str(i),
    #                 "jqMthod": "newsList",
    #                 "ouName": "",
    #             },
    #             callback=self.parse,
    #             meta={
    #                 "site_path_url": copy.deepcopy(self.start_urls[0])
    #             }
    #         )
    #     for i in range(1,5):
    #         yield scrapy.FormRequest(
    #             url="http://baowu.ouyeelbuy.com/baowu-shp/notice/bidMore?pageFlag=addSelect&pageSize=100",
    #             formdata={
    #                 "sDate": "",
    #                 "eDate": "",
    #                 "title": "",
    #                 "ouName": "",
    #                 "rfqMethod": "",
    #                 "cTeam": "",
    #                 "type": "bid",
    #                 "pageNow": str(i),
    #                 "jqMthod": "newsList",
    #             },
    #             meta={
    #                 "site_path_url": copy.deepcopy(self.start_urls[1])
    #             }
    #         )
    #
    #     for i in range(1, 5):
    #         yield scrapy.FormRequest(
    #             url="http://baowu.ouyeelbuy.com/baowu-shp/notice/bidMore?pageFlag=addSelect&pageSize=100",
    #             formdata={
    #                 "sDate": "",
    #                 "eDate": "",
    #                 "title": "",
    #                 "ouName": "",
    #                 "rfqMethod": "",
    #                 "cTeam": "",
    #                 "type": "purchase",
    #                 "pageNow": str(i),
    #                 "jqMthod": "newsList",
    #             },
    #             meta={
    #                 "site_path_url": copy.deepcopy(self.start_urls[2])
    #             }
    #         )

    def parse(self, response, **kwargs):
        item = {}
        json_text=ujson.loads(response.text)
        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..id')

        title_name_list = jsonpath.jsonpath(json_text, '$..projectName')

        title_date_list = jsonpath.jsonpath(json_text, '$..recCreateTime')

        for id1, title_name, title_date in zip(id1_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")

            item['title_url'] = f"http://rfq.ouyeelbuy.com/rfqNotice/entrustPublicityDetail?id={id1}&appCode=baowu"


            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)}
            )
    def parse_detail(self, response):
        item = response.meta['item']

        item['content_html'] = response.css(".left-bodys").get()
        yield item

    def parse1(self, response, **kwargs):
        item = {}
        json_text=ujson.loads(response.text)

        jsonText = jsonpath.jsonpath(json_text, '$..list')[0]
        # 提取 id的值
        id1_list = jsonpath.jsonpath(jsonText, '$..id')

        title_name_list = jsonpath.jsonpath(jsonText, '$..materialName')

        title_date_list = jsonpath.jsonpath(jsonText, '$..issueDate')

        for id1, title_name, title_date in zip(id1_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")
            item['title_url'] = f"https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/id={id1}/rfqMethod=RAQ/orgCode=UH0940/statusFlag=0"

            item['content_html']=httpx.get(url=item['title_url']).text
            yield item


    def parse_moreListb(self, response, **kwargs):
        item = {}
        json_text=ujson.loads(response.text)
        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..id')

        title_name_list = jsonpath.jsonpath(json_text, '$..supplierName')

        title_date_list = jsonpath.jsonpath(json_text, '$..issueDate')

        for id1, title_name, title_date in zip(id1_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)
            item['title_url'] = f"http://rfq.ouyeelbuy.com/rfqNotice/bidResListInfo?id={id1}&appCode=baowu"
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")
            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail_moreListb,
                meta={'item': copy.deepcopy(item)}
            )



    def parse_detail_moreListb(self, response):
        item = response.meta['item']

        item['content_html'] = response.css(".left-body").get()
        yield item

