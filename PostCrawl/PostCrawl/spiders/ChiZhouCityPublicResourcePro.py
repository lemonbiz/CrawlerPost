"""

池州市公共资源交易网

"""
import json
from copy import deepcopy

import jsonpath
import scrapy
from scrapy.http import JsonRequest


class ChizhoucitypublicresourceproSpider(scrapy.Spider):
    name = 'ChiZhouCityPublicResourcePro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://ggj.chizhou.gov.cn/front/bidcontent/9005001002',
        'http://ggj.chizhou.gov.cn/front/bidcontent/9005001004',
        'http://ggj.chizhou.gov.cn/front/bidcontent/9005002002',
        'http://ggj.chizhou.gov.cn/front/bidcontent/9005003001',
        'http://ggj.chizhou.gov.cn/front/bidcontent/9005004001',
        'http://ggj.chizhou.gov.cn/front/project/9005007008?tradeType=7&projectType=1',
        'http://ggj.chizhou.gov.cn/front/bidcontent/9005007001',
    ]

    @staticmethod
    def payload(i) -> dict:
        payload = {
            "filter": {"date": "", "regionCode": "", "tenderProjectType": "", "tenderMode": ""},
            "page": str(i),
            "rows": "100",
            "searchKey": "",
        }
        return payload

    def start_requests(self):
        # 1,2,3,4.... 对应的是start_urls
        yield from self.Request_data(self.start_urls[0], site_path_name="首页>交易信息>建设工程>招标公告", site_id="AA377B7148")
        yield from self.Request_data(self.start_urls[1], site_path_name="首页>交易信息>建设工程>中标结果公示", site_id="2E9B0C67BD")
        yield from self.Request_data(self.start_urls[2], site_path_name="首页 > 交易信息 > 政府采购 > 采购公告", site_id="1A4FE895AF")
        yield from self.Request_data(self.start_urls[3], site_path_name="网站首页 > 交易信息 > 土地矿权 > 出让公告",
                                     site_id="E12F72EAF0")

        yield from self.Request_data(self.start_urls[4], site_path_name="首页 > 交易信息 > 产权交易 > 交易公告", site_id="C9BF9DE798")
        yield from self.Request_data(self.start_urls[5], site_path_name="首页 > 交易信息 > 其他交易 > 项目登记", site_id="E3FFEACF3D")

        yield from self.Request_data(self.start_urls[6], site_path_name="首页 > 交易信息 > 其他交易 > 招标（采购）公告",
                                     site_id="8236EC8C12")

    def Request_data(self, site_path_url, site_path_name, site_id):
        yield JsonRequest(
            url=site_path_url,
            data=self.payload("1"),
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
        # 转换为json格式
        json_text = json.loads(response.text)
        # 用jsonpath 提取
        id_list = jsonpath.jsonpath(json_text, '$..id')
        date_list = jsonpath.jsonpath(json_text, '$..publishTime')
        title_name_list = jsonpath.jsonpath(json_text, '$..tenderProjectName')
        # 用zip函数遍历数据
        for id1, date, title_name in zip(id_list, date_list, title_name_list):

            if response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005001002":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005001002/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005001004":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005001004/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005002002":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005002002/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005002003":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005002003/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005002012":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005002012/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005003001":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005003001/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005003003":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005003003/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005004001":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/bidcontent/9005004001/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/project/9005007008?tradeType=7&projectType=1":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/project/9005007008/{id1}'
            elif response.url == "http://ggj.chizhou.gov.cn/front/bidcontent/9005007001":
                item['title_url'] = f'http://ggj.chizhou.gov.cn/front/project/9005007001/{id1}'

            item['title_name'] = str(title_name)
            item['title_date'] = str(date)
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_id'] = response.meta.get("site_id")
            item['site_path_name'] = response.meta.get("site_path_name")

            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item["content_html"] = response.xpath('//*[@id="printPanel"]').extract_first()
        yield item
