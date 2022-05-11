"""

包钢电子采购交易平台

"""

from copy import deepcopy

import scrapy

from PostCrawl.utils.Mixins import Mixins
from PostCrawl.utils.data_get import GetData


# class BaogangelectronicplatformSpider(scrapy.Spider):
#     name = 'BaoGangElectronicPlatform'
#     # allowed_domains = ['xxx.com']
#     start_urls = ['http://ep.btsteel.com/erp/mqm/jsp/mqmjNWC.jsp']
#
#     def start_requests(self):
#         for i in range(4,10):
#             yield scrapy.Request(
#                 url="http://ep.btsteel.com/erp/mqm/jsp/mqmjNWCList.jsp?inventoryType=&seqNo={}".format(i),
#                 callback=self.parse,
#                 meta={
#                     "site_path_url": deepcopy(self.start_urls[0]),
#                     "site_path_name": deepcopy("网采公告"),
#                     "site_id": deepcopy("DC58C98B30"),
#                 },
#                 dont_filter=True
#             )
#
#
#     def parse(self, response):
#         mx = Mixins()
#         gd = GetData()
#         for li in response.css("#mainPage2 > div"):
#
#             item = gd.data_get(response)
#             title_url: str = li.css('#rowDiv3 a::attr(href)').get()
#             if title_url is None:
#                 continue
#             item['title_url'] = mx.Get_domain_name(item['site_path_url'], title_url)
#             item['title_name'] = li.css('#rowDiv3 a::text').get()
#             item['title_date'] = li.css('#rowDiv4 a::text').get()
#
#             yield scrapy.Request(
#                 url=item['title_url'],
#                 callback=self.parse_detail,
#                 meta={
#                     "item":deepcopy(item)
#                 }
#             )
#
#     def parse_detail(self,response):
#         item =response.meta['item']
#
#         item['content_html']  =response.text
#         yield item