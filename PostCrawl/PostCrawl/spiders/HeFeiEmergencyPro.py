"""

合肥市应急管理局

"""

import copy
import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HefeiemergencyproSpider(scrapy.Spider):
    name = 'HeFeiEmergencyPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
                  'http://yjj.hefei.gov.cn/xxgk/awhgz/index.html',
                    "http://yjj.hefei.gov.cn/xxgk/tzgg/ggl/index.html",
                    "http://yjj.hefei.gov.cn/xxgk/yjjgz/index.html",
                    "http://yjj.hefei.gov.cn/yjxw/jcgz/index.html",
    ]
    script = """
    function main(splash,args)
      local url=args.url
      splash:set_user_agent("Mozilla/5.0Chrome/69.0.3497.100Safari/537.36")
      splash:go(url)
      splash:wait(2)
      splash:go(url)
      return{
      html=splash:html()
      }
    end
      """

    def start_requests(self):

        url_part1 = [
            'http://yjj.hefei.gov.cn/content/column/6788861?pageIndex=1'
        ]
        url_part2 = [
            'http://yjj.hefei.gov.cn/content/column/6788961?pageIndex=1'
        ]
        url_part3 = [
            'http://yjj.hefei.gov.cn/content/column/6788881?pageIndex=1'
        ]
        url_part4 = [
            'http://yjj.hefei.gov.cn/content/column/6788841?pageIndex=1'
        ]

        yield from self.handle_request(url_part1,self.start_urls[0], site_path_name='首页>信息公开>安委会工作', site_id='9ABF205476')
        yield from self.handle_request(url_part2,self.start_urls[1], site_path_name='首页>信息公开>通知公告>公告栏', site_id='85A708CE36')
        yield from self.handle_request(url_part3,self.start_urls[2], site_path_name='首页>信息公开>应急局工作', site_id='699380B675')
        yield from self.handle_request(url_part4,self.start_urls[3], site_path_name='首页>应急新闻>基层工作', site_id='2235A6F56F')

    def handle_request(self, url_list,site_path_url, site_path_name, site_id):
        for url in url_list:
            yield scrapy_splash.SplashRequest(
                url=url,
                callback=self.parse,
                endpoint="execute",
                args={
                    "lua_source": self.script,
                    "url": url,
                },
                meta={
                    "site_path_url": copy.deepcopy(site_path_url),
                    'site_path_name': site_path_name,
                    'site_id': site_id
                }
            )

    def parse(self, response, **kwargs):
        item = {}
        tr_list = response.css(".listnews ul li")
        for td in tr_list:
            item['title_name'] = td.css("a::attr(title)").get()
            item['title_url'] = td.css("a::attr(href)").get()
            item['title_date'] = td.css("span::text").get()
            item['site_path_url'] = response.meta.get("site_path_url")
            item['site_path_name'] = response.meta['site_path_name']
            item['site_id'] = response.meta['site_id']
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                callback=self.parse_detail,
                endpoint="execute",
                args={
                    "lua_source": self.script,
                    "url": item['title_url'],
                },
                meta={'item': copy.deepcopy(item)}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.css("#color_printsssss").get()

        if item['content_html'] is None:
            item['content_html'] = response.body.decode('utf-8')

        yield item

if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()