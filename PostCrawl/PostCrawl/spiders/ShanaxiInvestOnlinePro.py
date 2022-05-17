"""

全国投资项目在线审批监管平台-山西省

"""

import copy
import re
import time

import scrapy
import ujson as ujson
import jsonpath
import scrapy

from PostCrawl.utils.data_to_html import DataFormat


class ShanaxiinvestonlineproSpider(scrapy.Spider):
    name = 'ShanaxiInvestOnlinePro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/recordquery.jsp',
        'http://www.shanxitzxm.gov.cn/portalopenPublicInformation.do?method=queryExamineAll',
        'http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/historyProjectQuerySx.jsp',
    ]

    def start_requests(self):
        for i in range(1, 2):
            yield scrapy.FormRequest(
                url="http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=recordquery",
                formdata={
                    "condition": "",
                    "pageNo": str(i),
                },
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[0]),
                    "site_id": copy.deepcopy("95792497DE"),
                }
            )

        for i in range(1, 2):
            yield scrapy.FormRequest(
                url="http://www.shanxitzxm.gov.cn/portalopenPublicInformation.do?method=queryExamineAll",
                formdata={
                    "pageSize": "",
                    "pageNo": str(i),
                    "apply_project_name": "",
                },
                callback=self.parse1,
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[1]),
                    "site_id": copy.deepcopy("4ED6C2220E"),
                }
            )


        # for i in range(10, 500):
        #     yield scrapy.FormRequest(
        #         url="http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=historyProjectQuerySx",
        #         formdata={
        #             "condition": "",
        #             "pageNo": str(i),
        #         },
        #         callback=self.parse2,
        #         meta={
        #             "site_path_url": copy.deepcopy(self.start_urls[2]),
        #             "site_id": copy.deepcopy("CDBA3B3C0C"),
        #
        #         }
        #     )


    def parse(self, response, **kwargs):
        """
        http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=recordContentQuery
        """
        item = {}
        json_text = ujson.loads(response.text)

        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..projectuuid')

        title_name_list = jsonpath.jsonpath(json_text, '$..apply_project_name')

        title_date_list = jsonpath.jsonpath(json_text, '$..apply_time')

        for id1, title_name, title_date in zip(id1_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item['title_url'] = str(
                "http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=recordContentQuery/{}".format(id1))

            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_path_name'] = "信息公开>备案查询"
            item['site_id'] = response.meta.get('site_id')

            yield scrapy.FormRequest(
                url="http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=recordContentQuery",
                callback=self.parse_detail,
                formdata={
                    "projectuuid": id1
                },
                meta={
                    "item": copy.deepcopy(item)
                }
            )

    def parse1(self, response, **kwargs):
        item = {}
        for tr in response.css(".index-table tr"):

            item['title_name'] = tr.css("td:nth-child(1)::attr(title)").get()
            item['title_date'] = time.strftime('%Y-%m-%d')
            item['title_url'] = tr.css("td:nth-child(1) > a::attr(onclick)").get()

            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_path_name'] = "信息公开>批复公告"
            item['site_id'] = response.meta.get('site_id')

            try:
                item['title_url'] = re.findall("queryRecordContent\('(.*)',''\)", str(item['title_url']))[0]

                yield scrapy.FormRequest(
                    url="http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=recordContentQuery",
                    formdata={
                        "projectuuid": item['title_url']
                    },
                    callback=self.parse_detail,
                    meta={
                        "item": copy.deepcopy(item)
                    }
                )
            except Exception as e:
                print(e)

    def parse2(self, response, **kwargs):
        item = {}
        json_text = ujson.loads(response.text)

        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..deal_code')

        title_name_list = jsonpath.jsonpath(json_text, '$..apply_project_name')

        title_date_list = jsonpath.jsonpath(json_text, '$..apply_time')

        for id1, title_name, title_date in zip(id1_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_path_name'] = "信息公开>历史项目查询"
            item['site_id'] = response.meta.get("site_id")

            item['title_url'] = str(
                "http://www.shanxitzxm.gov.cn/portalopenapprovalResult.do?method=historyProjectQuerySx/{}".format(id1))

            item['content_html'] = str(json_text)

            yield item

    def parse_detail(self, response):
        item = response.meta['item']
        content_html = ujson.loads(response.text)
        tester = DataFormat()

        for con_item in content_html:
            data_dict = {
                "apply_project_name": con_item['apply_project_name'],
                "deal_code": con_item['deal_code'],
                "project_dept": con_item['project_dept'],
                "contact": con_item['contact'],
                "cor_type": con_item['cor_type'],
                "address_detial": con_item['address_detial'],
                "project_starttime": con_item['project_starttime'],
                "project_type": con_item['project_type'],
                "state": con_item['state'],
                "total_money": con_item['total_money'],
                "scale_content": con_item['scale_content'],
            }
            name_dict = {
                "apply_project_name": "项目名称",
                "deal_code": "项目代码",
                "project_dept": "单位名称",
                "contact": "项目法人：",
                "cor_type": "项目单位经济类型",
                "address_detial": "建设地点",
                "project_starttime": "计划开工时间",
                "project_type": "建设性质",
                "state": "审核状态",
                "total_money": "项目总投资（万元）",
                "scale_content": "主要建设规模及内容",
            }

            item['content_html'] = tester.dictToHtml(data_dict, name_dict)

        yield item


if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline
    file_name = os.path.basename(sys.argv[0])
    file_name=file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])
