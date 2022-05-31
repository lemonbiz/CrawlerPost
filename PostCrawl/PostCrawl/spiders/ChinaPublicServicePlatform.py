"""

中国招标投标公共服务平台

"""
import copy
import re

import scrapy_splash

import scrapy

from PostCrawl.utils.Mixins import Mixins
from PostCrawl.utils.data_get import GetData


class ChinapublicserviceplatformSpider(scrapy.Spider):
    name = 'ChinaPublicServicePlatform'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://bulletin.cebpubservice.com/xxfbcmses/search/change.html?searchDate=1997-01-06&dates=300&categoryId=89&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&word=',
        'https://bulletin.cebpubservice.com/xxfbcmses/search/result.html?searchDate=1997-01-06&dates=300&categoryId=90&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&word=',
        'https://bulletin.cebpubservice.com/xxfbcmses/search/candidate.html?searchDate=1997-01-06&dates=300&categoryId=91&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&word=',
        'https://bulletin.cebpubservice.com/xxfbcmses/search/qualify.html?searchDate=1997-01-06&dates=300&categoryId=92&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&word=',
        'https://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?searchDate=1997-03-25&dates=300&categoryId=88&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&word=',
    ]

    lua = \
        """
        function main(splash, args)
              splash:go(args.url)
              local scroll_to = splash:jsfunc("window.scrollTo")
              scroll_to(0, 2800)
              splash:set_viewport_full()
              splash:wait(5)
              return {html=splash:html()}
        end
        """

    def start_requests(self):
        cookies = Mixins().cookies_dict(
            "JSESSIONID=ABAEF6640EC5E447202F5A7795ED3F6F; BSFIT_mjvys=; BSFIT_5h1m4=; BSFIT_4omAv=; BSFIT_z4qCj=HLn03Ag1HCM23CHZ3N,HCzwHCzwHCzwHz; BSFIT_/khyt=pDQ0wytdCanLpR/0Cg,py/bpy/bpy/bp/,py/dCD/bpygdCY,pytKCR3bpDuaCY; BSFIT_zw05t=HKECJ5gAHKgCHASAJz,H5zXH5zXH5zXHz; BSFIT_s+yA0=z5vE4Avw9e324Azx9s,zAswzAswzAswzs; Hm_lvt_da6ebc493961b944c4bf10a22517a198=1648196602,1648431442,1648606268,1648877745; BSFIT_EXPIRATION=1648929391117; BSFIT_DEVICEID=UlK6MWkuQh2srHnAEeK2KV8rd9cxsCpwajKfE04Ro3UsFU-xYiCGcIa7A3K3i44vJ-0nTJKVNoFjwRyCzvNKsrEJ1r969tOLz2vxd6GQgFZKQEpsEl2SS-6-55rNSzxoj7bPGH4Z8ru5CvaEe_qhuNEtFgOCh14d; acw_tc=2760777416488777260607169e0c6c94e93ffb3a33082324c0929a58c1717d; route=2d537f5baec9369210a4429f0163a741; __ts=1648877947007; Hm_lpvt_da6ebc493961b944c4bf10a22517a198=1648877947; BSFIT_oj80x=m3Tav0bY9WkcmWo59b,m0oIv3kwm0kamo; ssxmod_itna=YuDtBKYIejOCGHD8b0IjGtGCmURGaRhPDsoDcDxA5D8D6DQeGTiX7D0D=GNG+wAnNDu7OqXTD21SBR=QbW8EUiDU4i8DCk7AehDenQD5xGoDPxDeDADYEjDAqiOD7qDdA1dsU8DbxYPnDA3Di4D+iTQDmqG0DDUFU4G2D7tnt7YCiL0LbQUYskA4HD=DjkbD/4pTujrWaPvM3QnPzOGqD0PzU=xC0g9v7i4V3rQDzL7DtkUB0dLYX16lAuX1mAmxmD4f3D4WtOAe3AqCK37dtAGG2OxatGxCm0GsWrv+fD5DG+y3SbD=; ssxmod_itna2=YuDtBKYIejOCGHD8b0IjGtGCmURGaRxikmozDumD0ybfe03Dc0ewFB24nRilU6rlbldBxFDGEB=KqH3CyjsPU1CH4pHZp7qNEMA++Hfsmk0k0KRWaAtOjx3d0R5pfU+hx/GydUc+AK7RojULv7900GWSj1QTKA4Q0wQw2wtD2xTGQw7hf6tRKKkbKdEMvosk5YkSfEWeau8ZLem43sSxTA/+xEKi4ayervSxRwR8mx2=jwYS0xDQxsKBDf9GxLjhcFU+YEIM3QTedXA8pxu6fki4=Ka4BAGUjE5EaOF=K0Tejlg2I1beBARamqN9vsD5IUR8QYfmh/+aV+beTAqpB/+uPVhleYf0WPHB0DAPuKfYbH9h4TWog5BUv=7EBiuNzYNUvQj4OCmY2Pq1pLD5UYR2ic0iIeobxNSCF80i8rxvuY4Ty7VR+N1KqXfaEOQj+WdBhKo3coaDvtV97FROH43V5kjgN/A8TEerMTx32IfTEfL9Dr1piR+N7DoD07eAHloPRgCEON3IPvLDtzCYoPD7=DYKbeD=")

        url_list_1 = [
            "https://bulletin.cebpubservice.com/xxfbcmses/search/change.html?searchDate=1997-04-02&dates=300&word=&categoryId=89&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}".format(
                i) for i in range(1, 100)]

        url_list_2 = [
            "https://bulletin.cebpubservice.com/xxfbcmses/search/result.html?searchDate=1997-04-02&dates=300&word=&categoryId=90&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}".format(
                i) for i in range(1, 100)]

        url_list_3 = [
            "https://bulletin.cebpubservice.com/xxfbcmses/search/candidate.html?searchDate=1997-04-02&dates=300&word=&categoryId=91&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}".format(
                i) for i in range(1, 100)]

        url_list_4 = [
            "https://bulletin.cebpubservice.com/xxfbcmses/search/qualify.html?searchDate=1997-04-02&dates=300&word=&categoryId=92&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}".format(
                i) for i in range(1, 100)]

        url_list_5 = [
            "https://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?searchDate=1997-04-02&dates=300&word=&categoryId=88&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}".format(
                i) for i in range(1, 100)]

        yield from self.handle_request(cookies, url_list_1, self.start_urls[0], site_path_name="更正公告公示",
                                       site_id="0F743A7AF1")  # change
        yield from self.handle_request(cookies, url_list_2, self.start_urls[1], site_path_name="中标结果公示",
                                       site_id="EAA2BE43F5")  # result
        yield from self.handle_request(cookies, url_list_3, self.start_urls[2], site_path_name="中标候选人公示",
                                       site_id="7577930FDC")  # candidate
        yield from self.handle_request(cookies, url_list_4, self.start_urls[3], site_path_name="资格预审公告",
                                       site_id="F24D5EF626")  # qualify
        yield from self.handle_request(cookies, url_list_5, self.start_urls[4], site_path_name="招标公告",
                                       site_id="C60E19BDF0")  # bulletin

    def handle_request(self, cookies, url_list_1, site_path_url, site_path_name, site_id):

        for url in url_list_1:
            yield scrapy_splash.SplashRequest(
                url=url,
                callback=self.parse,
                endpoint="execute",
                args={
                    "url": url,
                    "lua_source": self.lua,
                    "wait": 2
                },
                meta={
                    "site_path_url": copy.deepcopy(site_path_url),
                    "site_path_name": copy.deepcopy(site_path_name),
                    "site_id": copy.deepcopy(site_id),
                }
            )

    def parse(self, response, **kwargs):
        for tr in response.css(".table_text tr"):
            item = GetData().data_get(response)
            onclick = tr.css("td a::attr(href)").get()
            if onclick is None:
                continue

            onclick = tr.css("td a::attr(href)").get()

            item["title_url"] = re.search(r"""urlOpen\('(.*?)'\)""", onclick).group(1)
            if item['title_url'] is None:
                continue

            item['title_name'] = tr.css("td a::attr(title)").get()
            title_date: str = tr.css("td:nth-child(4)::text").get()
            item['title_date'] = title_date.replace("\t", '').replace('\n', '')

            yield scrapy_splash.SplashRequest(
                url=item["title_url"],
                endpoint="execute",
                args={
                    "url": item["title_url"],
                    "lua_source": self.lua,
                    "wait": 2
                },
                meta={"item": copy.deepcopy(item)},
                callback=self.parse_detail,
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css(".mian_list").get()
        yield item

if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline
    file_name = os.path.basename(sys.argv[0])
    file_name=file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])
