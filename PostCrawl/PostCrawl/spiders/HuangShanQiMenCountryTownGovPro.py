"""

祁门县人民政府

"""
import copy
import scrapy
import scrapy_splash

from PostCrawl.utils.data_get import GetData


class HuangshanqimencountrytowngovproSpider(scrapy.Spider):
    name = 'HuangShanQiMenCountryTownGovPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'https://www.ahqimen.gov.cn/zwgk/public/column/6615904?type=4&catId=6718758&action=list',
        'https://www.ahqimen.gov.cn/zwgk/public/column/6615904?type=4&catId=6718734&action=list',
        ]

    lua = """
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
        url_list_1=["https://www.ahqimen.gov.cn/huangshanzwgk/zwgk/site/label/8888?IsAjax=1&dataType=html&_=0.13205251332958068&labelName=publicInfoList&siteId=6793339&pageSize=20&pageIndex=1&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=200&organId=6615904&type=4&catId=6718734&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&keyWords=&file=%2Fc2%2Fhsxxgk%2FpublicInfoList_newest_hs"]

        url_list_2=["https://www.ahqimen.gov.cn/huangshanzwgk/zwgk/site/label/8888?IsAjax=1&dataType=html&_=0.6848924644121623&labelName=publicInfoList&siteId=6793339&pageSize=20&pageIndex=1&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=200&organId=6615904&type=4&catId=6718758&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&keyWords=&file=%2Fc2%2Fhsxxgk%2FpublicInfoList_newest_hs"]

        yield from self.handle_request(url_list_1,self.start_urls[0], site_path_name='首页>祁门县政府办>重大建设项目批准和实施>批准结果信息>建设项目环境影响评价审批', site_id='CB32946316')
        yield from self.handle_request(url_list_2,self.start_urls[1], site_path_name='首页 > 祁门县政府办 > 三大攻坚战 > 污染防治（生态环境） > 建设项目环境影响评价', site_id='C243062701')


    def handle_request(self, url_list,site_path_url, site_path_name, site_id):
        for url in url_list:
            yield scrapy_splash.SplashRequest(
                url=url,
                callback=self.parse,
                endpoint="execute",
                args={
                    "lua_source": self.lua,
                    "url": url
                },
                meta={
                    "site_path_url":copy.deepcopy(site_path_url),
                    'site_path_name': site_path_name,
                    'site_id': site_id
                }
            )

    def parse(self, response, **kwargs):
        item = {}
        title_list = response.xpath('/html/body/div[1]/ul/li')
        item['site_path_name'] = response.meta['site_path_name']
        item['site_id'] = response.meta['site_id']
        item['site_path_url'] = self.start_urls[0]
        for li in title_list:
            item["title_url"] = li.xpath('./a/@href').extract_first()
            item['title_name'] = li.xpath('./a/@title').extract_first()
            item['title_date'] = li.xpath('./span/text()').extract_first()
            item['site_path_url']= response.meta.get('site_path_url')
            yield scrapy_splash.SplashRequest(
                url=item['title_url'],
                endpoint="execute",
                callback=self.parse_detail,
                args={
                    "lua_source": self.lua,
                    "url": item['title_url'],
                },
                meta={'item': copy.deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item["content_html"] = response.xpath("//div[@class='secnr']").extract_first()

        if item['content_html'] is None:
            item['content_html'] = response.text
        yield item


if __name__ == '__main__':
    gd = GetData()
    gd.crawler_run()