"""

湖北省投资项目在线审批监管平台

"""

from copy import deepcopy

import scrapy

from PostCrawl.utils.data_get import GetData
from PostCrawl.utils.data_to_html import DataFormat


class HubeionlinegovernproSpider(scrapy.Spider):
    name = 'HuBeiOnlineGovernPro'
    # allowed_domains = ['xx.com']
    start_urls = [
        'http://tzxm.hubei.gov.cn/tzxmweb/pages/home/approvalResult/recordqueryNew.jsp',
        'http://tzxm.hubei.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityInfo.jsp',
        'http://tzxm.hubei.gov.cn/tzxmweb/pages/home/approvalResult/prePublicityInfo.jsp',

        # 批复公告
        'http://tzxm.hubei.gov.cn/portalopenPublicInformation.do?method=queryExamineAll',
    ]

    def start_requests(self):
        for i in range(1, 10):
            yield scrapy.FormRequest(
                url="http://tzxm.hubei.gov.cn/portalopenapprovalResult.do?method=recordqueryNew",
                callback=self.parse,
                formdata={
                    "condition": "",
                    "pageNo": str(i),
                },
                meta={
                    "site_path_url": deepcopy(self.start_urls[0]),
                    "site_path_name": deepcopy("信息公开>批后公开>备案查询"),
                    "site_id": deepcopy("589E4D23FB"),
                },
            )

        for i in range(1,5):
            yield scrapy.FormRequest(
                url="http://tzxm.hubei.gov.cn/portalopenPublicInformation.do?method=getPublicityList",
                callback=self.parse_accep,
                formdata={
                    "publicity_type": "1",
                    "condition": "",
                    "pageNo": str(i),
                },
                meta={
                    "site_path_url": deepcopy(self.start_urls[1]),
                    "site_path_name": deepcopy("信息公开>受理公告"),
                    "site_id": deepcopy("6ED95EE583"),
                },
            )

        for i in range(1,5):
            yield scrapy.FormRequest(
                url="http://tzxm.hubei.gov.cn/portalopenPublicInformation.do?method=getPublicityList",
                callback=self.parse_appr,
                formdata={
                    "publicity_type": "2",
                    "condition": "",
                    "pageNo": str(i),
                },
                meta={
                    "site_path_url": deepcopy(self.start_urls[2]),
                    "site_path_name": deepcopy("信息公开>拟批准公示"),
                    "site_id": deepcopy("30B234B837"),
                },
            )


        for i in range(1,100):
            yield scrapy.FormRequest(
                url="http://tzxm.hubei.gov.cn/portalopenPublicInformation.do?method=queryExamineAllNew&type=queryPublicresultNew.jsp",
                callback=self.parse_Public,
                formdata={
                    "pageSize": "10",
                    "pageNo": str(i),
                    "apply_project_name": "",
                },
                meta={
                    "site_path_url": deepcopy(self.start_urls[3]),
                    "site_path_name": deepcopy("信息公开>批后公开>批复公告"),
                    "site_id": deepcopy("4501E9BAA8"),
                },
            )

    def parse(self, response):
        for data in response.json()[0]['list']:
            item = GetData().data_get(response)
            item['title_name'] = data['apply_project_name']
            item['title_date'] = data['apply_time']
            projectuuid = data['projectuuid']
            item[
                'title_url'] = f"http://tzxm.hubei.gov.cn/portalopenapprovalResult.do?method=recordContentQuery/{projectuuid}"

            yield scrapy.FormRequest(
                url="http://tzxm.hubei.gov.cn/portalopenapprovalResult.do?method=recordContentQuery",
                formdata={
                    "projectuuid": projectuuid
                },
                meta={
                    "item": deepcopy(item)
                },
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        item = response.meta['item']
        tester = DataFormat()
        data = response.json()[0]
        try:
            data_dict = {
                "deal_code": data['deal_code'],
                "result": data['result'],
                "apply_time": data['apply_time'],
                "scale_content": data['scale_content'],
                "cor_type": data['cor_type'],
                "address_detial": data['address_detial'],
                "state": data['state'],
                "internet_mode": data['internet_mode'],
                "is_foreign": data['is_foreign'],
                "project_dept": data['project_dept'],
                "contact": data['contact'],
                "project_type": data['project_type'],
                "item_person": data['item_person'],
                "catalog_code": data['catalog_code'],
                "project_starttime": data['project_starttime'],
                "introduction_use": data['introduction_use'],
                "apply_project_name": data['apply_project_name'],
                "construction_mode": data['construction_mode'],
                "projectuuid": data['projectuuid'],
                "total_money": data['total_money'],
                "industry_name": data['industry_name'],
            }

            name_dict = {
                "deal_code": "deal_code",
                "result": 'result',
                "apply_time": 'apply_time',
                "scale_content": 'scale_content',
                "cor_type": 'cor_type',
                "address_detial": 'address_detial',
                "state": 'state',
                "internet_mode": 'internet_mode',
                "is_foreign": 'is_foreign',
                "project_dept": 'project_dept',
                "contact": 'contact',
                "project_type": 'project_type',
                "item_person": 'item_person',
                "catalog_code": 'catalog_code',
                "project_starttime": 'project_starttime',
                "introduction_use": 'introduction_use',
                "apply_project_name": 'apply_project_name',
                "construction_mode": 'construction_mode',
                "projectuuid": 'projectuuid',
                "total_money": 'total_money',
                "industry_name": 'industry_name',
            }

            content_html = tester.dictToHtml(data_dict, name_dict)
        except KeyError as e:
            content_html = "值错误"
        item['content_html'] = content_html
        yield item

    def parse_accep(self, response):
        for data in response.json()[0]['JSONObject']['rowSet']['primary']:
            item = GetData().data_get(response)
            item['title_name'] = data['apply_project_name']
            item['title_date'] = data['start_date_tochar']

            if item['title_date'] is None:
                item['title_date'] = data['deal_time_tochar']

            item['title_url'] = f"http://tzxm.hubei.gov.cn/tzxmweb/acceptancePublicityDetail.do?" \
                                f"publicity_id={data['publicity_id']}&" \
                                f"projectuuid={data['projectuuid']}" \
                                f"&item_id={data['item_id']}" \
                                f"&sendid={data['sendid']}" \
                                f"&publicity_type=1"
            # item['title_url'] = f"https://tzxm.shaanxi.gov.cn/tzxmspweb/api/admin/service/sbsp/apprtprojectinfo/selectApprtProjectInfoByDealState?pageSize=10&pageNo=1&search=2205-610721-04-01-262897"
            tester = DataFormat()

            # for k,v in data.items():

            content_html = tester.dictToHtml(data)
            item['content_html'] = content_html
            yield item


    def parse_appr(self,response):
        for data in response.json()[0]['JSONObject']['rowSet']['primary']:
            item = GetData().data_get(response)
            item['title_name'] = data['apply_project_name']
            item['title_date'] = data['start_date_tochar']
            item['title_url'] = f"http://tzxm.hubei.gov.cn/tzxmweb/acceptancePublicityDetail.do?" \
                                f"publicity_id={data['publicity_id']}&" \
                                f"projectuuid={data['projectuuid']}" \
                                f"&item_id={data['item_id']}" \
                                f"&sendid={data['sendid']}"
            # item['title_url'] = f"https://tzxm.shaanxi.gov.cn/tzxmspweb/api/admin/service/sbsp/apprtprojectinfo/selectApprtProjectInfoByDealState?pageSize=10&pageNo=1&search=2205-610721-04-01-262897"
            tester = DataFormat()

            # for k,v in data.items():

            content_html = tester.dictToHtml(data)
            item['content_html'] = content_html
            yield item


    def parse_Public(self,response):
        for tr in response.css(".index-table tr"):
            item = GetData().data_get(response)
            item["title_name"]=tr.css("td::attr(title)").get()
            if item['title_name'] is None:
                continue
            item["title_url"]=tr.css("td a::attr(onclick)").get()
            if item['title_url'] is None:
                item["title_url"]=tr.css("td:nth-child(1)::text").get()

            item["title_date"]=tr.css("td:last-child::text").get()
            item['content_html'] = "暂无数据"

            yield item




if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])
