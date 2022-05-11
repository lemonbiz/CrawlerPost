"""

欧冶工业品

"""
import copy

import httpx
import jsonpath
import scrapy
import ujson

from PostCrawl.utils.Mixins import Mixins


class ShanghaiouyebiddingbussinessSpider(scrapy.Spider):
    name = 'ShangHaiOuYeBiddingBussiness'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://www.ouyeelbuy.com/ouyeelbuy-web/purchase?flag=bid']

    def start_requests(self):
        m = Mixins()

        # cookies = m.cookies_dict(
        #     "Hm_lvt_367132120e814f91c937d2f1aca27704=1648029552,1648084426,1648517189; JSESSIONID=6B7B1EC60D7804B209AA0D20457720E0; HMF_CI=9ce1eb1570cd33dcb34f0bc3381bb33156ed6ce4f4eae9242f39051d4a1a8be36d; gr_user_id=c82fd66d-8e4c-49f4-942c-87cd6ed900d9; zg_did=%7B%22did%22%3A%20%2217f95a82f0f84c-09923558d41065-9771539-1fa400-17f95a82f10afc%22%7D; zg_182ad3cf8fc343c0bdb676c46c8b0dc5=%7B%22sid%22%3A%201648519696501%2C%22updated%22%3A%201648520416615%2C%22info%22%3A%201648517284701%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E6%AC%A7%E8%B4%9D%E9%97%A8%E6%88%B7-%E8%AF%B8%E8%91%9Bio%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201648519696501%2C%22landHref%22%3A%20%22http%3A%2F%2Frfq.ouyeelbuy.com%2FrfqNotice%2FbidListInfo%3Fid%3Dc08c65e2-af01-11ec-906d-005056b12bb8%22%7D; HMY_JC=a3c6e80ae69d602363a1469742afe16335c6be9a366452fa2dbead601c34aa4c9a")

        yield scrapy.FormRequest(
            url="https://www.ouyeelbuy.com/ouyeelbuy-web/notice/purchaseMore?pageFlag=addSelect&pageSize=10",
            # cookies=cookies,
            formdata={
                "sDate": "issueDate",
                "eDate": "DESC",
                "ouName": "",
                "rfqMethod": "",
                "publicBiddingFlag": "",
                "type": "purchase",
                "pageNow": "1",
                "jqMthod": "newsList",
            },
            callback=self.parse,
        )

    def parse(self, response, **kwargs):
        item = {}
        json_text = ujson.loads(response.text)
        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..id')
        id2_list = jsonpath.jsonpath(json_text, '$..uuCode')

        title_name_list = jsonpath.jsonpath(json_text, '$..title')

        title_date_list = jsonpath.jsonpath(json_text, '$..issueDate')

        for id1, title_name, title_date, uuCode in zip(id1_list, title_name_list, title_date_list, id2_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item[
                'title_url'] = f"https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/id={id1}/rfqMethod=RAQ/orgCode={uuCode}/statusFlag=0"

            item['content_html'] = httpx.get(item['title_url']).text
            item['site_path_url'] = self.start_urls[0]
            item['site_id'] = "F37358EE03"
            item['site_path_name'] = "采购公告"

            yield item

    #         yield scrapy.Request(
    #             url=str(item['title_url']),
    #             meta={
    #                 'item': copy.deepcopy(item),
    #                   },
    #             callback=self.parse_detail,
    #         )
    #
    #
    # def parse_detail(self, response):
    #     item = response.meta.get('item')
    #     item['content_html'] = response.text
    #
    #     yield item
