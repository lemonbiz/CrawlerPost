"""

抚顺市生态环境局

"""
import copy
import json
import jsonpath
import scrapy
import scrapy_splash


class FushuncityecologicalenvironproSpider(scrapy.Spider):
    name = 'FuShunCityEcologicalEnvironPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://sthj.fushun.gov.cn/dynamic/zwgk/nohandsdate_govInfoPub.html?categorynum=003006',
                  'http://sthj.fushun.gov.cn/dynamic/zwgk/nohandsdate_govInfoPub.html?categorynum=003005']

    # def start_requests(self):
    #     for i in range(1,5):
    #         script = """
    #             function main(splash, args)
    #               local json = require("json")
    #             local response = splash:http_post{
    #               "http://sthj.fushun.gov.cn/EWB-FRONT/rest/lightfrontaction/getgovinfolist",
    #               body=json.encode({categorynum="003006",pageIndex=%d,pageSize=20,siteGuid="3373428a-5c73-4318-83c9-32cf98fea0d3"}),
    #               headers={["content-type"]="application/json"}
    #             }
    #             return response.body
    #             end
    #            """%i
    #
    #         yield from self.hand_lua_request(script,self.start_urls[0])
    #     script = """
    #         function main(splash, args)
    #           local json = require("json")
    #         local response = splash:http_post{
    #           "http://sthj.fushun.gov.cn/EWB-FRONT/rest/lightfrontaction/getgovinfolist",
    #           body=json.encode({categorynum="003005",pageIndex=0,pageSize=20,siteGuid="3373428a-5c73-4318-83c9-32cf98fea0d3"}),
    #           headers={["content-type"]="application/json"}
    #         }
    #         return response.body
    #         end
    #        """
    #     yield from self.hand_lua_request(script,self.start_urls[1])
    def start_requests(self):
        script = """
            function main(splash, args)
              local json = require("json")
            local response = splash:http_post{
              "http://sthj.fushun.gov.cn/EWB-FRONT/rest/lightfrontaction/getgovinfolist", 
              body=json.encode({categorynum="003006",pageIndex=1,pageSize=20,siteGuid="3373428a-5c73-4318-83c9-32cf98fea0d3"}),
              headers={["content-type"]="application/json"}
            }
            return response.body
            end
           """

        yield from self.hand_lua_request(script,self.start_urls[0], site_path_name='双随机一公开', site_id='E14EA0938C')
        script = """
            function main(splash, args)
              local json = require("json")
            local response = splash:http_post{
              "http://sthj.fushun.gov.cn/EWB-FRONT/rest/lightfrontaction/getgovinfolist", 
              body=json.encode({categorynum="003005",pageIndex=0,pageSize=20,siteGuid="3373428a-5c73-4318-83c9-32cf98fea0d3"}),
              headers={["content-type"]="application/json"}
            }
            return response.body
            end
           """
        yield from self.hand_lua_request(script,self.start_urls[1], site_path_name='政策与解读', site_id='67554324FF')

    def hand_lua_request(self, script,site_path_url, site_path_name, site_id):
        url = "http://sthj.fushun.gov.cn/EWB-FRONT/rest/lightfrontaction/getgovinfolist"
        yield scrapy_splash.SplashRequest(
            method="POST",
            url=url,
            callback=self.parse,
            endpoint="execute",
            args={
                "lua_source": script,
                "url": url,
            },
            meta={
                "site_path_url": copy.deepcopy(site_path_url),
                'site_path_name': site_path_name,
                'site_id': site_id
            }
        )

    def parse(self, response, **kwargs):
        item = GetData().data_get(response)
        m = Mixins()

        json_text = json.loads(response.text)
        # 提取 id的值
        url_list = jsonpath.jsonpath(json_text, '$..infourl')

        title_name_list = jsonpath.jsonpath(json_text, '$..title')

        title_date_list = jsonpath.jsonpath(json_text, '$..infodate')
        item['site_path_name'] = response.meta['site_path_name']
        item['site_id'] = response.meta['site_id']

        for url, title_name, title_date in zip(url_list, title_name_list, title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item['title_url'] = m.Get_domain_name(self.start_urls[0],url)

            item['site_path_url'] = response.meta.get("site_path_url")



            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.xpath('//*[@id="container"]/div[2]/div[2]').extract_first()
        # print(item['title_name'], item['title_date'], item['title_url'])
        yield item


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()