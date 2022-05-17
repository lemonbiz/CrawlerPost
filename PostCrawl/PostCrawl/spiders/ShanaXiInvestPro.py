"""

全国投资项目在线审批监管平台-山西省

"""

import copy
import scrapy_splash
import ujson as ujson
import jsonpath
import scrapy


class ShanaxiinvestproSpider(scrapy.Spider):
    name = 'ShanaXiInvestPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityInfo.jsp',
        'http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/prePublicityInfo.jsp',
    ]

    def start_requests(self):
        for i in range(1, 3):
            yield scrapy.FormRequest(
                url="http://www.shanxitzxm.gov.cn/portalopenPublicInformation.do?method=getPublicityList",
                formdata={
                    "publicity_type": "1",
                    "condition": "",
                    "pageNo": str(i),
                },
                callback=self.parse,
                meta={
                    "site_path_url": copy.deepcopy(self.start_urls[0]),
                    'site_id':"1BDF895021"
                }
            )


        # for i in range(1, 2):
        #     yield scrapy.FormRequest(
        #         url="http://www.shanxitzxm.gov.cn/portalopenPublicInformation.do?method=getPublicityList",
        #         formdata={
        #             "publicity_type": "2",
        #             "condition": "",
        #             "pageNo": str(i),
        #         },
        #         callback=self.parse_1,
        #         meta={
        #             "site_path_url": copy.deepcopy(self.start_urls[1]),
        #             'site_id': "4264F299E4"
        #         }
        #     )

    def parse(self, response, **kwargs):
        """
        http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityDetail.jsp?publicity_id=a2a7855dd3724a96b2ec90e68b8ed0b3&projectuuid=0cdfe6b60c9846369e494c67ea4cf5ca&item_id=3BDE0541334D4AED8AA602A7686C147D&sendid=75f338c8713b4e0ead4a6f04124702e5&publicity_type=1
        http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityDetail.jsp?publicity_id=69f1c0d90cec44928c8c1efeeabe5c5f&projectuuid=b67c9a6cd020413281b73b577eb1ff3e&item_id=3BDE0541334D4AED8AA602A7686C147D&sendid=131e0e342cad4850bde51780b61102df&publicity_type=1

        """
        item = {}
        json_text = ujson.loads(response.text)
        lua = """
            function main(splash, args)
              splash:go(args.url)
              local scroll_to = splash:jsfunc("window.scrollTo")
              scroll_to(0, 2800)
              splash:set_viewport_full()
              splash:wait(5)
              return {html=splash:html()}
            end
        """
        # 提取 id的值
        id1_list = jsonpath.jsonpath(json_text, '$..publicity_id')
        id2_list = jsonpath.jsonpath(json_text, '$..projectuuid')
        id3_list = jsonpath.jsonpath(json_text, '$..item_id')
        id4_list = jsonpath.jsonpath(json_text, '$..sendid')

        title_name_list = jsonpath.jsonpath(json_text, '$..apply_project_name')

        title_date_list = jsonpath.jsonpath(json_text, '$..deal_time_tochar')

        for id1, id2, id3, id4, title_name, title_date in zip(id1_list, id2_list, id3_list, id4_list, title_name_list,
                                                              title_date_list):
            item['title_name'] = str(title_name)
            item['title_date'] = str(title_date)

            item[
                'title_url'] = f"http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityDetail.jsp?publicity_id={id1}&projectuuid={id2}&item_id={id3}&sendid={id4}&publicity_type=1"

            # 将目录地址 传值到管道中
            item['site_path_url'] = response.meta.get('site_path_url')

            if response.url == self.start_urls[0]:
                # 目录名
                item["site_path_name"] = '信息公开>受理公告'
            else:
                item["site_path_name"] = '信息公开>拟批准公示'

            item['site_id'] = response.meta.get('site_id')
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                args={
                    "url": item['title_url'],
                    "lua_source": lua,
                },
                callback=self.parse_detail,
                meta={
                    "item": copy.deepcopy(item)
                }
            )

    # def parse_1(self, response, **kwargs):
    #     """
    #     http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityDetail.jsp?publicity_id=a2a7855dd3724a96b2ec90e68b8ed0b3&projectuuid=0cdfe6b60c9846369e494c67ea4cf5ca&item_id=3BDE0541334D4AED8AA602A7686C147D&sendid=75f338c8713b4e0ead4a6f04124702e5&publicity_type=1
    #     http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/acceptancePublicityDetail.jsp?publicity_id=69f1c0d90cec44928c8c1efeeabe5c5f&projectuuid=b67c9a6cd020413281b73b577eb1ff3e&item_id=3BDE0541334D4AED8AA602A7686C147D&sendid=131e0e342cad4850bde51780b61102df&publicity_type=1
    #
    #     """
    #     item = {}
    #     json_text = ujson.loads(response.text)
    #     lua = """
    #         function main(splash, args)
    #           splash:go(args.url)
    #           local scroll_to = splash:jsfunc("window.scrollTo")
    #           scroll_to(0, 2800)
    #           splash:set_viewport_full()
    #           splash:wait(5)
    #           return {html=splash:html()}
    #         end
    #     """
    #     # 提取 id的值
    #     id1_list = jsonpath.jsonpath(json_text, '$..publicity_id')
    #     id2_list = jsonpath.jsonpath(json_text, '$..projectuuid')
    #     id3_list = jsonpath.jsonpath(json_text, '$..item_id')
    #     id4_list = jsonpath.jsonpath(json_text, '$..sendid')
    #
    #     title_name_list = jsonpath.jsonpath(json_text, '$..apply_project_name')
    #
    #     title_date_list = jsonpath.jsonpath(json_text, '$..deal_time_tochar')
    #
    #     for id1, id2, id3, id4, title_name, title_date in zip(id1_list, id2_list, id3_list, id4_list, title_name_list,
    #                                                           title_date_list):
    #         item['title_name'] = str(title_name)
    #         item['title_date'] = str(title_date)
    #
    #         item[
    #             'title_url'] = f"http://www.shanxitzxm.gov.cn/tzxmweb/pages/home/approvalResult/prePublicityDetail.jsp?publicity_id={id1}&projectuuid={id2}&item_id={id3}&sendid={id4}&flag=0"
    #
    #         # 将目录地址 传值到管道中
    #         item['site_path_url'] = response.meta.get('site_path_url')
    #
    #         if response.url == self.start_urls[0]:
    #             # 目录名
    #             item["site_path_name"] = '信息公开>受理公告'
    #         else:
    #             item["site_path_name"] = '信息公开>拟批准公示'
    #
    #         item['site_id'] = response.meta.get('site_id')
    #         yield scrapy_splash.SplashRequest(
    #             url=item['title_url'],
    #             endpoint="execute",
    #             args={
    #                 "url": item['title_url'],
    #                 "lua_source": lua,
    #             },
    #             callback=self.parse_detail,
    #             meta={
    #                 "item": copy.deepcopy(item)
    #             }
    #         )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = str(response.css("#detailinfo").get())

        yield item


if __name__ == '__main__':
    import sys
    import os
    from scrapy import cmdline

    file_name = os.path.basename(sys.argv[0])
    file_name = file_name.split(".")[0]
    cmdline.execute(['scrapy', 'crawl', file_name])
