"""

ppp项目信息监测服务平台

"""
import copy
import json
import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData

gd = GetData()


class PppprojectinfoproSpider(scrapy.Spider):
    name = 'PPPProjectInfoPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://60.29.59.189:1380/tianjininvestpppmonitor-front#/main/projectannouncement']

    def start_requests(self):
        yield scrapy.Request(
            method="POST",
            url="http://60.29.59.189:1380/tianjininvest-ppp-python/ppp-project-inquiry/publicity/list",
            body=json.dumps({
                "condition": {
                    "affiliating_area_name": "",
                    "project_name": "",
                    "sort": "desc"
                },
                "page": "1",
                "size": "10",
            }),
            headers={'Content-Type': 'application/json;charset=UTF-8'},
            callback=self.parse,
            meta={
                "site_path_url": copy.deepcopy(self.start_urls[0]),
                "site_path_name": copy.deepcopy("项目公示"),
                "site_id": copy.deepcopy("BB603B2629"),
            }
        )

    def parse(self, response, **kwargs):
        script = """
                function main(splash, args)
                  splash:go(args.url)
                  local scroll_to = splash:jsfunc("window.scrollTo")
                  scroll_to(0, 2800)
                  splash:set_viewport_full()
                  splash:wait(5)
                  return {html=splash:html()}
                end
        """

        for data in response.json()['data']['content']:
            item = gd.data_get(response)
            item['title_name'] = data['project_name']
            item['title_date'] = data['impl_scheme_check_time']
            item['site_path_url'] = self.start_urls[0]
            item['title_url'] = str(
                'http://60.29.59.189:1380/tianjininvestpppmonitor-front#/main/projectannouncement/detail/{}').format(
                data['ppp_id'])

            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                args={
                    "lua_source": script,
                    "url": item['title_url'],
                },
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css(".contentCon3upxI8").get()
        yield item


if __name__ == '__main__':
    gd.crawler_run()
