"""
甘肃省自然资源厅

"""
import copy
import operator

import jsonpath
import scrapy
import scrapy_splash
import ujson

from PostCrawl.utils.data_get import GetData


class GansunatureresourceproSpider(scrapy.Spider):
    name = 'GanSuNatureResourcePro'
    # allowed_domains = ['xxx.com']
    start_urls = [
                  'http://zrzy.gansu.gov.cn/zrzy/c116317/xxgk_list.shtml',
                  'http://zrzy.gansu.gov.cn/zrzy/c110607/xxgk_list.shtml',
                  'http://zrzy.gansu.gov.cn/zrzy/c107675/xxgk_list.shtml',
                  'http://zrzy.gansu.gov.cn/zrzy/c107676/xxgk_list.shtml',
                  'http://fzgg.gansu.gov.cn/fzgg/c109768/zfxxgkzd.shtml',
                  'http://fzgg.gansu.gov.cn/fzgg/c109752/zfxxgkzd.shtml',
                  'http://sthj.gansu.gov.cn/sthj/c105992/xxgk_list.shtml',
                  'http://sthj.gansu.gov.cn/sthj/c105991/xxgk_list.shtml',
                  'http://sthj.gansu.gov.cn/sthj/c105990/xxgk_list.shtml',
                  ]

    def start_requests(self):
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
        url_list: list = [
                             "http://zrzy.gansu.gov.cn/common/search/9ba4562fc4cb4d628d5395df05e03480?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/647408fb7b404f1bb8f3ab3647f4430c?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/59900679a8444ff7a446fbe3d9411a35?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/098515bd59b141c49e42163a2bb7de1f?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/7e6cd86cc7ce44f8a490920f4d242dab?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/3c5e76a67624457c863c977bcc36b877?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/7cfa6365343e4f69b13f0ade298c0580?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                         "http://zrzy.gansu.gov.cn/common/search/1af3f735a45b44bcbbb60eefae010f29?_isAgg=true&_isJson"
                          "=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1",
                             "http://zrzy.gansu.gov.cn/common/search/c9a02f69b99040ceafb03493e6c5756c?_isAgg=true&_isJson=true"
                             "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1"]

        for url in url_list:
            url: str = url
            yield scrapy_splash.SplashRequest(
                url=url,
                endpoint="execute",
                args={
                    "url": url,
                    "lua_source": lua,
                },
                callback=self.parse
            )

    # def start_requests(self):
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
    #     url_list: list = [
    #                          "http://zrzy.gansu.gov.cn/common/search/9ba4562fc4cb4d628d5395df05e03480?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 20)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/647408fb7b404f1bb8f3ab3647f4430c?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 19)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/59900679a8444ff7a446fbe3d9411a35?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 18)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/098515bd59b141c49e42163a2bb7de1f?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 99)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/7e6cd86cc7ce44f8a490920f4d242dab?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 2)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/3c5e76a67624457c863c977bcc36b877?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 6)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/7cfa6365343e4f69b13f0ade298c0580?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 22)] + \
    #                      ["http://zrzy.gansu.gov.cn/common/search/1af3f735a45b44bcbbb60eefae010f29?_isAgg=true&_isJson" \
    #                       "=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                       range(1, 14)] + \
    #                      [
    #                          "http://zrzy.gansu.gov.cn/common/search/c9a02f69b99040ceafb03493e6c5756c?_isAgg=true&_isJson=true" \
    #                          "&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}".format(i) for i in
    #                          range(1, 23)]
    #
    #     for url in url_list:
    #         url: str = url
    #         yield scrapy_splash.SplashRequest(
    #             url=url,
    #             endpoint="execute",
    #             args={
    #                 "url": url,
    #                 "lua_source": lua,
    #             },
    #             callback=self.parse
    #         )

    def parse(self, response, **kwargs):
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
        item = {}
        json_text = response.xpath("/html/body//text()").extract_first()
        ujson_text = ujson.loads(json_text)
        # 提取 id的值
        url_list = jsonpath.jsonpath(ujson_text, '$..url')

        title_name_list = jsonpath.jsonpath(ujson_text, '$..title')

        title_date_list = jsonpath.jsonpath(ujson_text, '$..publishedTimeStr')
        # print(id_list,title_name_list,title_date_list)
        for url, title_name, title_date in zip(url_list, title_name_list, title_date_list):
            item['title_name']: str = title_name
            item['title_date']: str = title_date

            item['title_url']: str = f"http://zrzy.gansu.gov.cn{url}"

            if operator.contains(str(item['title_url']), "c116317"):
                item['site_path_url'] = self.start_urls[0]
                item['site_path_name'] = "首页>矿业权市场"
                item['site_id'] = "FF771C3DCF"
            elif operator.contains(str(item['title_url']), "c107675"):
                item['site_path_url'] = self.start_urls[2]
                item['site_path_name'] = "机关公文"
                item['site_id'] = "764E420E09"
            elif operator.contains(str(item['title_url']), "c107676"):
                item['site_path_url'] = self.start_urls[3]
                item['site_path_name'] = "首页>中长期规划"
                item['site_id'] = "9EFADC6DA7"
            elif operator.contains(str(item['title_url']),"c109768"):
                item['site_path_url'] = self.start_urls[4]
                item['site_path_name'] = "首页>中长期规划"
                item['site_id'] = "10683B24D7"
            elif operator.contains(str(item['title_url']),"c109752"):
                item['site_path_url'] = self.start_urls[5]
                item['site_path_name'] = "首页>重大项目审批核准备案信息"
                item['site_id'] = "7745B2D961"
            elif operator.contains(str(item['title_url']),"c105992"):
                item['site_path_url'] = self.start_urls[6]
                item['site_path_name'] = "首页>政府信息公开>法定主动公开内容>重点领域信息公开>建设项目环评>批准项目公告"
                item['site_id'] = "C819612177"
            elif operator.contains(str(item['title_url']),"c105991"):
                item['site_path_url'] = self.start_urls[7]
                item['site_path_name'] = "拟批准项目公示"
                item['site_id'] = "B4EBD188BC"
            elif operator.contains(str(item['title_url']),"c105990"):
                item['site_path_url'] = self.start_urls[8]
                item['site_path_name'] = "首页>政府信息公开>法定主动公开内容>重点领域信息公开>建设项目环评>建设项目环境影响评价文件的审批"
                item['site_id'] = "94ADCFD70D"

            # operator.contains(str(item['title_url']), "c110607")
            else :
                item['site_path_url'] = self.start_urls[1]
                item['site_path_name'] = "规范性文件"
                item['site_id'] = "7A32C2A738"


            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                callback=self.parse_detail,
                args={
                    "url": url,
                    "lua_source": lua,
                    "wait": 1
                },
                meta={'item': copy.deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css(".xinxigongkai_main").get()

        if item['content_html'] is None:
            item['content_html'] = response.text

        yield item


if __name__ == '__main__':
    import os
    os.system("scrapy crawl GanSuNatureResourcePro")