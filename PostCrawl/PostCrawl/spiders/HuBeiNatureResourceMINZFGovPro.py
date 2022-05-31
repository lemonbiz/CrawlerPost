from copy import deepcopy

import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData

class HubeinatureresourceminzfgovproSpider(scrapy.Spider):
    name = 'HuBeiNatureResourceMINZFGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = ['http://zrzyt.hubei.gov.cn/fbjd/tzgg/',
                  'http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/zykcpjgjcxxgs/',
                  'http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/yc/',
                  'http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/lc/',
                  'http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/gz/',
                  ]

    def start_requests(self):
        yield from self.handle_request(
            "http://zrzyt.hubei.gov.cn/fbjd/tzgg/",
            site_path_url="http://zrzyt.hubei.gov.cn/fbjd/tzgg/",
            site_path_name="首页>政府信息公开>通知公告",
            site_id="DE5C1F9E72",
        )

        yield from self.handle_request(
            "http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/zykcpjgjcxxgs/",
            site_path_url="http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/zykcpjgjcxxgs/",
            site_path_name="首页>部门动态>专题专栏>矿产资源储量与利用管理信息公示>主要矿产品价格监测信息公示",
            site_id="A4E74BC397",
        )

        yield from self.handle_request(
            f"http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/yc/",
            site_path_url="http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/yc/",
            site_path_name="首页>部门动态>专题专栏>矿产资源储量与利用管理信息公示>矿业权出让收益评估公示>一次",
            site_id="6545F0CFBD",
        )

        yield from self.handle_request(
            "http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/lc/",
            site_path_url="http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/lc/",
            site_path_name="首页>部门动态>专题专栏>矿产资源保护监督>矿业权出让收益评估公示>两次",
            site_id="7053DC5A32",
        )

        yield from self.handle_request(
            f"http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/gz/index.shtml",
            site_path_url="http://zrzyt.hubei.gov.cn/bmdt/ztzl/kczyclylyglxxgs/kyqcrsypggs/gz/",
            site_path_name="首页>部门动态>专题专栏>矿产资源储量与利用管理信息公示>矿业权出让收益评估公示>告知",
            site_id="7EE7D8C164",
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
        for li in response.css("#share li"):
            item = GetData().data_get(response)
            item["title_url"] = li.css("a::attr(href)").get()

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
                },
                dont_filter=True,
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css(".article").get()
        # 标题名
        item['title_name'] = response.css('meta[name="ArticleTitle"]::attr(content)').get()
        # 标题时间
        item['title_date'] = response.css('meta[name="PubDate"]::attr(content)').get()
        yield item


if __name__ == '__main__':
    GetData().crawler_run()
