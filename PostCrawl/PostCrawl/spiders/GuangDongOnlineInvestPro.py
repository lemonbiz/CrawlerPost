"""
	全国投资项目在线审批监管平台-广东省
"""
import time
from copy import deepcopy

import scrapy
from scrapy.http import JsonRequest

from PostCrawl.utils.Mixins import Mixins
from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class GuangdongonlineinvestproSpider(scrapy.Spider):
    name = 'GuangDongOnlineInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#']

    gd = GetData()
    def start_requests(self):
        # 备案公开
        yield from self.handle_request(
            "https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA",
            "1",
            "1",
            "https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#",
            "备案公开",
            "4DC4047EFA"
        )

        # 备案项目
        yield from self.handle_request(
            "https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA",
            "2",
            "1",
            "https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#",
            "备案项目撤回",
            "4DC4047EFA"
        )

        # 核准项目公告
        yield from self.handle_request(
            "https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA",
            "10",
            "1",
            "https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#",
            "核准项目公告",
            "4DC4047EFA"
        )

        # 审批项目公告
        yield from self.handle_request(
            "https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageSP",
            "7",
            "1",
            "https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#",
            "审批项目公告",
            "4DC4047EFA"
        )

        # 节能审查公告
        yield from self.handle_request(
            "https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectJnscByPage",
            "13",
            "1",
            "https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#",
            "节能审查公告",
            "4DC4047EFA"
        )

    def handle_request(self,url,flag,pageNumber,site_path_url,site_path_name,site_id):
        # 备案公开
        yield JsonRequest(
            url=url,
            data={
                "flag": flag,
                "nameOrCode": "",
                "pageSize": "15",
                "city": "",
                "pageNumber": pageNumber
            },
            callback=self.parse,
            meta={
                "site_path_url": deepcopy(site_path_url),
                "site_path_name": deepcopy(
                    site_path_name),
                "site_id": deepcopy(site_id),

            },
            dont_filter=True
        )

    def parse(self, response):
        tester = DataFormat()

        for data in response.json()['data']['list']:
            item = GetData().data_get(response)
            print(data)
            item['title_name'] = data['projectName']
            item['title_url'] = f"https://gd.tzxm.gov.cn/PublicityInformation/resultDetail/{data['projectName']}.html"
            item['title_date'] = data['submitDate']

            data_dict = {
                "备案项目编号	": data['proofOrSerialCode'],
                "项目名称": data['projectName'],
                "项目所在地": data['place'],
                "项目总投资": str(data['totalInvest'])+"万元",
                "项目规模及内容": data['scope'],
                "建设单位": data['applyOrgan'],
                "备案机关": data['fullName'],
                "备案申报日期	": data['submitDate'],
                "复核通过日期": data['submitDate'],
                "终止年限": data['overDate'],
                "项目当前状态": data['stateFlagName'],
            }
            # name_dict = {
            #     "issueDate": "发布日期",
            #     "title": "标题名称",
            #     "issueUsername": "发布人",
            #     "materialName": "项目介绍",
            #     "deliveryAddress": "公司地点",
            # }
            content_html = tester.dictToHtml(data_dict)

            item['content_html'] = content_html
            yield item


if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])