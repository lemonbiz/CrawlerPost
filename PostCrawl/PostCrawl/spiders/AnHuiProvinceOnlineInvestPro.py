import re

import scrapy

from PostCrawl.utils.data_get import GetData, HandleRequest


class AnhuiprovinceonlineinvestproSpider(scrapy.Spider):
    name = 'AnHuiProvinceOnlineInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://tzxm.ahzwfw.gov.cn/portalopenPublicInformation.do?method=queryExamineAll']


    hr = HandleRequest()
    gd = GetData()

    def start_requests(self):
        for i in range(1,20):
            yield from self.hr.FormPost(
                url="http://tzxm.ahzwfw.gov.cn/portalopenPublicInformation.do?method=queryExamineAll",
                callback=self.parse,
                formdata={
                    "pageSize": "20",
                    "pageNo": str(i),
                    "apply_project_name": "",
                    "projectInfo.areaDetialCode": "",
                    "projectInfo.projectAddress": "",
                    "projectInfo.areaDetial": "",
                    "projectInfo.industryId": "",
                    "projectInfo.industry": "",
                },
                site_path_url="http://tzxm.ahzwfw.gov.cn/portalopenPublicInformation.do?method=queryExamineAll",
                site_path_name="公示信息>办理结果公示",
                site_id="52622C4946"
            )

    def parse(self, response):
        item=self.gd.data_get(response)
        for tr in response.css("#publicInformationForm tr"):
            onclick=tr.css("td a::attr(onclick)").get()

            pattern = re.match("window\.open\(\'(.*?)\'\)",onclick)

            if pattern is None:
                continue

            item['title_url'] ="http://tzxm.ahzwfw.gov.cn/"+str(pattern.group(1))
            item['title_name'] = tr.css("td a::text").get()
            item['title_date']=tr.css("td:nth-child(5)::text").get()

            yield from self.gd.detail_response(self.parse_detail,item)

    def parse_detail(self,response):
        yield from self.gd.detail_get_data(response,".content_main")

if __name__ == '__main__':
    GetData().crawler_run()