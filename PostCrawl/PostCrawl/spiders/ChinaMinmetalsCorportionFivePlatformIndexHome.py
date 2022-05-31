"""

中国五矿集团有限公司采购电子商务平台

"""
import json

import scrapy
import ujson
from scrapy.http import JsonRequest

from PostCrawl.utils.data_get import GetData


# class ChinaminmetalscorportionfiveplatformindexhomeSpider(scrapy.Spider):
#     name = 'ChinaMinmetalsCorportionFivePlatformIndexHome'
#     # allowed_domains = ['xxx.com']
#     start_urls = [
#         'http://ec.mcc.com.cn/logonAction.do',
#         'http://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=88720997EE833F5C0D4F75AA51055EBF32A0B8F4E80A2EDBD9E727247694C887&xxposition=zbgg',
#         'http://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=88720997EE833F5C3C90A83DBB48268E04C8988918ECF8ACC6CA41737B6EFF68&xxposition=cgxx',
#
#     ]
#
#     def start_requests(self):
#         yield scrapy.Request(
#             url="http://ec.mcc.com.cn/logonAction.do",
#             callback=self.parse,
#             meta={
#                 "site_path_url": self.start_urls[0],
#                 "site_path_name": "首页> 采购信息；首页>采购公告 ；首页>变更公告 ；首页>结果公告",
#                 "site_id": "A5B5F21C82",
#             }
#
#         )
#
#     def parse(self, response, **kwargs):
#         for ul in response.css("#tab111 > dl > dd > ul > div > ol > li"):
#             item = GetData().data_get(response)
#             # 获得 采购信息|采购公告|变更公告|结果公告 可变化的 码  然后封装到 url中
#             item["title_name"] = ul.css(".left a::attr(title)").get()
#             title_url: str = ul.css(".left a::attr(onclick)").get()
#             item["title_date"] = ul.css(".right::text").get()
#
#             #  判断是否包含 招标这个字符
#             if operator.contains(str(item["title_name"]), "招标"):
#                 try:
#                     title_url_code = re.findall("showZbsMessage\('(.*)'\)", str(title_url))[0]
#                 except IndexError:
#                     title_url_code = str(item["title_name"])
#                 item[
#                     "title_url"] = "http://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showZbsDetail&inviteid={}".format(
#                     title_url_code)
#                 yield from self.call_func(item)
#
#             #  判断是否包含 中标这个字符
#             elif operator.contains(str(item["title_name"]), "中标"):
#                 try:
#                     title_url_code = re.findall("showZhongbggMessage\('(.*)'\)", str(title_url))[0]
#                 except IndexError:
#                     title_url_code = str(item["title_name"])
#                 item[
#                     "title_url"] = "http://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showZhongbggDetail&xxbh={}&inviteid=undefined".format(
#                     title_url_code)
#                 yield from self.call_func(item)
#
#             #  判断是否包含 澄清这个字符
#             elif operator.contains(str(item["title_name"]), "澄清"):
#                 try:
#                     title_url_code = re.findall("""onclick=\"showCqggMessage\('(.*)'\)\"""", str(title_url))[0]
#                 except IndexError:
#                     title_url_code = str(item["title_name"])
#                 item[
#                     "title_url"] = "http://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showCqggDetail&xxbh={}".format(
#                     title_url_code)
#                 yield from self.call_func(item)
#
#             #  判断是否包含 资格预审这个字符
#             elif operator.contains(str(item["title_name"]), "资格预审"):
#                 try:
#                     title_url_code = re.findall("showZgysDetail\('(.*)'\)", str(title_url))[0]
#                 except IndexError:
#                     title_url_code = str(item["title_name"])
#                 item[
#                     "title_url"] = "http://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showZgysDetail&zgyswjbm={}".format(
#                     title_url_code)
#                 yield from self.call_func(item)
#
#             else:
#                 yield None
#
#     def call_func(self, item):
#         yield scrapy.Request(
#             url=item["title_url"],
#             meta={
#                 "item": copy.deepcopy(item)
#             },
#             callback=self.parse_detail
#         )
#
#     # def call_func(self, item, lua):
#     # yield scrapy_splash.SplashRequest(
#     #     url=item["title_url"],
#     #     endpoint="execute",
#     #     args={
#     #         "url": item["title_url"],
#     #         "lua_source": lua,
#     #     },
#     #     meta={
#     #         "item": copy.deepcopy(item)
#     #     },
#     #     callback=self.parse_detail:
#
#     # )
#
#     def parse_detail(self, response):
#         item = response.meta.get("item")
#
#         item["content_html"] = response.css(".main-news").get()
#
#         if item["content_html"] is None:
#             item["content_html"] = "付费板块 暂无权限查看"
#         # print(item)
#         yield item
