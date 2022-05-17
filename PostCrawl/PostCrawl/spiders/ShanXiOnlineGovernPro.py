"""

全国投资项目在线审批监管平台-陕西省

"""

from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class ShanxionlinegovernproSpider(scrapy.Spider):
    name = 'ShanXiOnlineGovernPro'
    # allowed_domains = ['xx.com']
    start_urls = ['https://tzxm.shaanxi.gov.cn/tzxmspweb/phgs']

    def start_requests(self):

        for i in range(1,15):
            url=f"https://tzxm.shaanxi.gov.cn/tzxmspweb/api/admin/service/sbsp/apprtprojectinfo/selectApprtProjectInfoByDealState?pageSize=100&pageNo={i}"
            yield scrapy.FormRequest(
                url=url,
                callback=self.parse,
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    "site_path_name": deepcopy("首页>>信息公开>>批后公示>（办理结果公示 & 备案查询）"),
                    "site_id": deepcopy("73FA58F29E"),
                }
            )

    def parse(self, response):
        tester = DataFormat()
        for data in response.json()["data"]['objList']:
            item = GetData().data_get(response)
            item['title_name'] = data['applyProjectName']
            item['title_date'] = data['items'][0]['approvalDate']
            item['title_url'] = f"https://tzxm.shaanxi.gov.cn/tzxmspweb/phgs/{data['dealCode']}"
            # item['title_url'] = f"https://tzxm.shaanxi.gov.cn/tzxmspweb/api/admin/service/sbsp/apprtprojectinfo/selectApprtProjectInfoByDealState?pageSize=10&pageNo=1&search=2205-610721-04-01-262897"

            try:
                data_dict = {
                    "dealDeptName": data['items'][0]['dealDeptName'],
                    "deptName": data['items'][0]['deptName'],
                    "approveType": data['items'][0]['approveType'],
                    "obtainresultText": data['items'][0]['obtainresultText'],
                    "approvalDate": data['items'][0]['approvalDate'],
                    "dealState": data['items'][0]['dealState'],
                    "exchangeTime": data['items'][0]['exchangeTime'],
                    "auditType": data['items'][0]['auditType'],
                    "realFinishTime": data['items'][0]['realFinishTime'],
                    "projectUuid": data['items'][0]['projectUuid'],
                    "rownum": data['items'][0]['rownum'],
                    "itemName": data['items'][0]['itemName'],
                    "dealStateText": data['items'][0]['dealStateText'],
                    "dealCode": data['items'][0]['dealCode'],
                    "auditTypeText": data['items'][0]['auditTypeText'],
                    "applyProjectName": data['items'][0]['applyProjectName'],
                    "obtainresult": data['items'][0]['obtainresult'],
                    "deptCode": data['items'][0]['deptCode'],
                }

                name_dict = {
                    "dealDeptName": "dealDeptName",
                    "deptName": "deptName",
                    "approveType": "approveType",
                    "obtainresultText": "obtainresultText",
                    "approvalDate": "approvalDate",
                    "dealState": "dealState",
                    "exchangeTime": "exchangeTime",
                    "auditType": "auditType",
                    "realFinishTime": "realFinishTime",
                    "projectUuid": "projectUuid",
                    "rownum": "rownum",
                    "itemName": "itemName",
                    "dealStateText": "dealStateText",
                    "dealCode": "dealCode",
                    "auditTypeText": "auditTypeText",
                    "applyProjectName": "applyProjectName",
                    "obtainresult": "obtainresult",
                    "deptCode": "deptCode",
                }
                content_html = tester.dictToHtml(data_dict, name_dict)
            except KeyError as e:
                content_html = "值错误"
            item['content_html'] = content_html
            yield item

if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])