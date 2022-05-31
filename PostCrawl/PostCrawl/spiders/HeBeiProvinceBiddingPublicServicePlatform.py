import scrapy

from PostCrawl.utils.data_get import GetData, HandleRequest


class HebeiprovincebiddingpublicserviceplatformSpider(scrapy.Spider):
    name = 'HeBeiProvinceBiddingPublicServicePlatform'
    # allowed_domains = ['xxx.com']
    start_urls = [
        'http://www.hebeieb.com/tender/xxgk/list.do?selectype=zbgg',
        'http://www.hebeieb.com/tender/xxgk/list.do?selectype=dygs',
        'http://www.hebeieb.com/tender/xxgk/list.do?selectype=bggg',
        'http://www.hebeieb.com/tender/xxgk/list.do?selectype=kbjl',
        'http://www.hebeieb.com/tender/xxgk/list.do?selectype=pbgs',
        'http://www.hebeieb.com/tender/xxgk/list.do?selectype=zhongbgg',

    ]

    hr = HandleRequest()

    def start_requests(self):
        for i in range(1, 20):
            yield from self.hr.FormPost(
                url="http://www.hebeieb.com/tender/xxgk/zbgg.do",
                formdata={
                    "page": str(i),
                    "TimeStr": "",
                    "allDq": "",
                    "allHy": "reset1",
                    "AllPtName": "",
                    "KeyStr": "",
                    "KeyType": "ggname",
                },
                callback=self.parse,
                site_path_url='http://www.hebeieb.com/tender/xxgk/list.do?selectype=zbgg',
                site_path_name='招标公告',
                site_id='DCB44526C2',
            )

        for i in range(1, 20):
            yield from self.hr.FormPost(
                url="http://www.hebeieb.com/tender/xxgk/bggg.do",
                formdata={
                    "page": str(i),
                    "TimeStr": "",
                    "allDq": "",
                    "allHy": "reset1",
                    "AllPtName": "",
                    "KeyStr": "",
                    "KeyType": "ggname",
                },
                callback=self.parse,
                site_path_url='http://www.hebeieb.com/tender/xxgk/list.do?selectype=bggg',
                site_path_name='变更公告',
                site_id='6DDAEB52D3'
            )

        for i in range(1, 20):
            yield from self.hr.FormPost(
                url="http://www.hebeieb.com/tender/xxgk/dygs.do",
                formdata={
                    "page": str(i),
                    "TimeStr": "",
                    "allDq": "",
                    "allHy": "reset1",
                    "AllPtName": "",
                    "KeyStr": "",
                    "KeyType": "ggname",
                },
                callback=self.parse,
                site_path_url='http://www.hebeieb.com/tender/xxgk/list.do?selectype=dygs',
                site_path_name='答疑澄清',
                site_id='7AD12E1D85'
            )

        for i in range(1, 20):
            yield from self.hr.FormPost(
                url="http://www.hebeieb.com/tender/xxgk/kbjl.do",
                formdata={
                    "page": str(i),
                    "TimeStr": "",
                    "allDq": "",
                    "allHy": "reset1",
                    "AllPtName": "",
                    "KeyStr": "",
                    "KeyType": "ggname",
                },
                callback=self.parse,
                site_path_url='http://www.hebeieb.com/tender/xxgk/list.do?selectype=kbjl',
                site_path_name='开标记录',
                site_id='959C51D785'
            )

        for i in range(1, 20):
            yield from self.hr.FormPost(
                url="http://www.hebeieb.com/tender/xxgk/pbgs.do",
                formdata={
                    "page": str(i),
                    "TimeStr": "",
                    "allDq": "",
                    "allHy": "reset1",
                    "AllPtName": "",
                    "KeyStr": "",
                    "KeyType": "ggname",
                },
                callback=self.parse,
                site_path_url='http://www.hebeieb.com/tender/xxgk/list.do?selectype=pbgs',
                site_path_name='中标候选人公示',
                site_id='2896AD38B9'
            )

        for i in range(1, 20):
            yield from self.hr.FormPost(
                url="http://www.hebeieb.com/tender/xxgk/zhongbgg.do",
                formdata={
                    "page": str(i),
                    "TimeStr": "",
                    "allDq": "",
                    "allHy": "reset1",
                    "AllPtName": "",
                    "KeyStr": "",
                    "KeyType": "ggname",
                },
                callback=self.parse,
                site_path_url='http://www.hebeieb.com/tender/xxgk/list.do?selectype=zhongbgg',
                site_path_name='中标结果公示',
                site_id='6F54FA0CCC'
            )

    gd = GetData()

    def parse(self, response):
        for h4 in response.css(".publicont div h4"):
            item = self.gd.data_get(response)
            item['title_url'] = "http://www.hebeieb.com/" + str(h4.css("a::attr(href)").get())
            item['title_name'] = h4.css("a::text").get()
            item['title_date'] = h4.css("span::text").get()
            yield from self.gd.detail_response(self.parse_detail, item)

    def parse_detail(self, response):
        yield from self.gd.detail_get_data(response, ".con_row")


if __name__ == '__main__':
    GetData().crawler_run()
