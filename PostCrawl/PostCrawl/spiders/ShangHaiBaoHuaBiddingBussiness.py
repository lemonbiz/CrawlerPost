"""

欧贝易购/上海宝华国际招标有限公司
"""
from copy import deepcopy

import jsonpath
import scrapy
import ujson
from scrapy.http import JsonRequest

from PostCrawl.utils.data_get import HandleRequest


class ShanghaibaohuabiddingbussinessSpider(scrapy.Spider):
    name = 'ShangHaiBaoHuaBiddingBussiness'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://qiye.ouyeelbuy.com/bhzb/noticeListMore?type=1',
        'https://qiye.ouyeelbuy.com/bhzb/noticeListMore?type=2',
        'https://qiye.ouyeelbuy.com/bhzb/noticeListMore?type=3',
    ]

    def start_requests(self):
        url_1 = [
            "https://qiye.ouyeelbuy.com/bhzb/cmsZBloadNotice?title=&issueDateStart=&issueDateEnd=&callBidsNum=&flag=0&type=1&page=1&jqMethod=purchase&rows=50"]
        url_2 = [
            "https://qiye.ouyeelbuy.com/bhzb/cmsZBloadNotice?title=&issueDateStart=&issueDateEnd=&callBidsNum=&flag=0&type=2&page=1&jqMethod=purchase&rows=50"]
        url_3 = [
            "https://qiye.ouyeelbuy.com/bhzb/cmsZBloadNotice?title=&issueDateStart=&issueDateEnd=&callBidsNum=&flag=0&type=3&page=1&jqMethod=purchase&rows=50"]

        yield from self.Json(self.parse, url_1, site_path_url=self.start_urls[0],site_id = "859B5378D3",site_path_name = "欧贝易购|招标")
        yield from self.Json(self.parse, url_2, site_path_url=self.start_urls[1], site_id = "397566A0D2",site_path_name = "中标结果")
        yield from self.Json(self.parse, url_3, site_path_url=self.start_urls[2],site_id = "3697084B57",site_path_name = "变更公告")


    def Json(self, callback, url_list, site_path_url,site_id,site_path_name, data=None):
        for url in url_list:
            yield JsonRequest(
                url=url,
                data=data,
                callback=callback,
                meta={
                    "site_path_url": deepcopy(site_path_url),
                    "site_id":deepcopy(site_id),
                    "site_path_name":deepcopy(site_path_name),
                }
            )
    # def start_requests(self):
    #
    #     url_1=["https://qiye.ouyeelbuy.com/bhzb/cmsZBloadNotice?title=&issueDateStart=&issueDateEnd=&callBidsNum=&flag=0&type=1&page={}&jqMethod=purchase&rows=10".format(i)for i in range(1,10)]
    #     url_2=["https://qiye.ouyeelbuy.com/bhzb/cmsZBloadNotice?title=&issueDateStart=&issueDateEnd=&callBidsNum=&flag=0&type=2&page={}&jqMethod=purchase&rows=10".format(i)for i in range(1,10)]
    #     url_3=["https://qiye.ouyeelbuy.com/bhzb/cmsZBloadNotice?title=&issueDateStart=&issueDateEnd=&callBidsNum=&flag=0&type=3&page={}&jqMethod=purchase&rows=10".format(i)for i in range(1,10)]
    #     url_list = url_1+url_2+url_3
    #     for url in url_list:
    #         yield JsonRequest(
    #             url=url,
    #             callback=self.parse
    #         )

    def parse(self, response, **kwargs):
        item = {}
        json_text = ujson.loads(response.text)

        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..id')

        title_name_list = jsonpath.jsonpath(json_text, '$..title')

        title_date_list = jsonpath.jsonpath(json_text, '$..createDate')
        content_html_list = jsonpath.jsonpath(json_text, '$..mainBody')

        for id1, title_name, title_date, content_html in zip(id1_list, title_name_list, title_date_list,
                                                             content_html_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)
            item['title_url'] = f"https://qiye.ouyeelbuy.com/bhzb/queryNoticeDetail?id={id1}"
            item['content_html'] = str(content_html)
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")
            yield item
