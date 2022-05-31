from copy import deepcopy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HubeinatureresourcemingovproSpider(scrapy.Spider):
    name = 'HuBeiNatureResourceMINGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://zrzyt.hubei.gov.cn/fbjd/zhengce/zcjd/index.shtml',
                    'http://zrzyt.hubei.gov.cn/fbjd/xxgkml/ggzypz/kyqcrzrxxgsgk/#test',
                  ]

    def start_requests(self):
        yield from self.handle_request(
            "http://zrzyt.hubei.gov.cn/fbjd/zhengce/zcjd/index.shtml",
            site_path_url="http://zrzyt.hubei.gov.cn/fbjd/zhengce/zcjd/index.shtml",
            site_path_name="政策解读",
            site_id="13CF042709",
        )
        yield from self.handle_request(
            "http://zrzyt.hubei.gov.cn/fbjd/xxgkml/ggzypz/kyqcrzrxxgsgk/#test",
            site_path_url="http://zrzyt.hubei.gov.cn/fbjd/xxgkml/ggzypz/kyqcrzrxxgsgk/#test",
            site_path_name="首页>政府信息公开>法定主动公开内容>公共资源配置>矿业权出让",
            site_id="E1B52ADD4A",
        )

    def handle_request(self, url, site_path_url, site_path_name, site_id):
        yield scrapy_splash.SplashRequest(
            url=url,
            endpoint="execute",
            args={
                "url": url,
                "lua_source": self.lua,
            },
            callback=self.parse,
            meta={
                "site_path_url": deepcopy(site_path_url),
                "site_path_name": deepcopy(site_path_name),
                "site_id": deepcopy(site_id),
            },
        )

    lua = \
        """
        function main(splash,args)
              local url=args.url
              splash:set_user_agent("Mozilla/5.0Chrome/69.0.3497.100Safari/537.36")
              splash:go(url)
              splash:wait(2)
              splash:go(url)
              return{
              html=splash:html(),
              png = splash:png()
              }
        end

        """

    def parse(self, response):
        for li in response.css(".info-list li"):
            item = GetData().data_get(response)
            item["title_url"]=li.css("a::attr(href)").get()
            item['title_date'] = li.css("span::text").get()
            item['title_name'] = li.css("a::text").get()
            if item['title_url'] is None:
                continue
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                args={
                    "url": item['title_url'],
                    "lua_source": self.lua,
                },
                callback=self.parse_detail,
                meta={
                    "item": deepcopy(item)
                }
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css(".article").get()
        yield item


if __name__ == '__main__':
    GetData().crawler_run()
