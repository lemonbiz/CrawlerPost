import scrapy
from scrapy.http import JsonRequest


class BeedingbiaobussinessproSpider(scrapy.Spider):
    name = 'BeeDingBiaoBussinessPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://www.mafengs.com/purchases/search?query=']

    def start_requests(self):
        yield JsonRequest(
            url="https://www.mafengs.com/purchases/search",
            data={'pageNumber': '2',
                  'pageSize': '25',
                  'provinceId': '0',
                  'searchType': 'TITLE',
                  'sourceTimeEnd': '1652162186',
                  'sourceTimeStart': '1620626186'},
            headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://www.mafengs.com',
                'referer': 'https://www.mafengs.com/',
                'sec-ch-ua': 'Not A;Brand;v=99, Chromium;v=101, Google Chrome;v=101',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'TE': 'trailers',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
                'x-from-url': 'https://www.mafengs.com/purchases/search',
                'x-sign': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiODg0YzkzZGVkMTYxYzNhY2FlZDhjNDJmNjM2OTZlMiIsIm5iZiI6MTY1MjE2MzA1NywiaWF0IjoxNjUyMTYzMDU3LCJleHAiOjE2NTIxNjMwNjd9.O6ek3FcSRNTKWlSbxvETX-AaVL1OlRoF7r6pu3Cx1Uo'
            },
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response):
        print(response.json())
