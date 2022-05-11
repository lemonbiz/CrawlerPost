'''
河北省投资项目在线审批监管平台
'''
import copy
import re

import scrapy


class HebeiinvestmentproSpider(scrapy.Spider):
    name = 'HeBeiInvestMentPro'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://tzxm.hbzwfw.gov.cn/sbglweb/channelContentListpt',
        'http://tzxm.hbzwfw.gov.cn/sbglweb/channelContentList',
    ]

    def start_requests(self):
        for i in range(2):
            channelID = 'A8FE5F40FFFFFFFFEB4F9270FFFFFFBF'
            yield from self.handle_request(channelID, i, self.start_urls[1], site_id="9266C683CF")

        for i in range(2):
            channelID = '402881da5215a653015215be1eea033f'
            yield from self.handle_request(channelID, i, self.start_urls[0], site_id="6C0F5C9316")

    def handle_request(self, channelID, i, site_path_url, site_id):
        yield scrapy.FormRequest(
            url=site_path_url,
            formdata={
                'channelID': channelID,
                'query': '请输入关键字',
                'rows': '10',
                'page': str(i + 1),
            },
            callback=self.parse,
            meta={
                "site_path_url": copy.deepcopy(site_path_url),
                "site_id": copy.deepcopy(site_id),
            }
        )

    def parse(self, response, **kwargs):
        # pass
        item = {}
        title_ul = response.xpath('//*[@id="content"]/div/div[4]/ul/li')
        url_id = response.xpath('//*[@id="content"]/div/div[4]/ul/li/a/@href').extract()
        date_list = response.xpath('//*[@id="content"]/div/div[4]/ul/li')

        for title, id, date in zip(title_ul, url_id, date_list):
            content_id = re.findall(r"ptdtInfo\?channelID=A8FE5F40FFFFFFFFEB4F9270FFFFFFBF&contentID=(.*)", id)[0]
            item['title_name'] = title.xpath('./a/text()').extract_first()
            title_date = date.xpath('./span/text()').extract_first()
            item['title_date'] = re.sub('\t\t', '', title_date).replace('\r\n', '')

            item['title_url'] = 'http://tzxm.hbzwfw.gov.cn/sbglweb/ptdtInfoN?contentID={}'.format(content_id)

            # 将目录地址 传值到管道中
            item['site_path_url'] = response.meta.get('site_path_url')

            if response.url == self.start_urls[0]:
                # 目录名
                item["site_path_name"] = '首页 > 政策法规'
            else:
                item["site_path_name"] = '首页 > 平台动态'

            item['site_id'] = response.meta.get('site_id')

            yield scrapy.Request(
                url=item['title_url'],
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)},
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['content_html'] = response.text
        yield item


if __name__ == '__main__':
    import os

    os.system("scrapy crawl HeBeiInvestMentPro")
