# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Optional

from .api_manager.script_api import APIManager
from .api_manager.script_data import SpiderData
import httpx
from loguru import logger
import time


class PostcrawlPipeline:

    def __init__(self):
        # 网站名
        self.site_name: Optional[str] = None
        # 栏目名
        self.title_type: Optional[str] = None


    def process_item(self, item, spider):
        # 鞍钢招标有限公司
        if spider.name == 'AnGangZhaoBiaoBussinessPro':
            # 政府单位名
            self.site_name = '鞍钢招标有限公司'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 鞍钢集团电子招标投标交易平台
        elif spider.name == 'AnGangZhaoBiaoBussinessPro_first':
            # 政府单位名
            self.site_name = '鞍钢集团电子招标投标交易平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 鞍钢招标有限公司商机|寻源
        elif spider.name == 'AnGangZhaoBiaoBussinessPro_Second':
            # 政府单位名
            self.site_name = '鞍钢招标有限公司商机|寻源'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 河北省投资项目在线审批监管平台
        elif spider.name == 'HeBeiInvestMentPro':
            # 政府单位名
            self.site_name = '河北省投资项目在线审批监管平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 全国投资项目在线审批监管平台-山西省
        elif spider.name == 'ShanaxiInvestOnlinePro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-山西省'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 全国投资项目在线审批监管平台-山西省
        elif spider.name == 'ShanaXiInvestPro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-山西省'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 欧贝易购/上海宝华国际招标有限公司
        elif spider.name == 'ShangHaiBaoHuaBiddingBussiness':
            # 政府单位名
            self.site_name = '欧贝易购/上海宝华国际招标有限公司'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 中国宝武采购专区/欧冶工业品
        elif spider.name == 'ShangHaiBaoWuBiddingBussiness':
            # 政府单位名
            self.site_name = '欧贝易购/上海宝华国际招标有限公司'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 欧冶工业品
        elif spider.name == 'ShangHaiOuYeBiddingBussiness':
            # 政府单位名
            self.site_name = '欧冶工业品'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 山西省招标投标公共服务平台
        elif spider.name == 'ShanXiProvinceTenderingBiddingPro':
            # 政府单位名
            self.site_name = '山西省招标投标公共服务平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 马鞍山市公共资源交易网
        elif spider.name == 'MaAnShanCityPublicResourcePro':
            # 政府单位名
            self.site_name = '马鞍山市公共资源交易网'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 池州市公共资源交易网
        elif spider.name == 'ChiZhouCityPublicResourcePro':
            # 政府单位名
            self.site_name = '池州市公共资源交易网'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 铜化集团电子招标采购平台_优质采
        elif spider.name == 'TongLingElectronicBussiness':
            # 政府单位名
            self.site_name = '铜化集团电子招标采购平台_优质采'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 铜陵有色集团电子采购（招投标）系统
        elif spider.name == 'TongLinYouSeMetalPro':
            # 政府单位名
            self.site_name = '铜陵有色集团电子采购（招投标）系统'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 中国招标投标公共服务平台
        elif spider.name == 'ChinaPublicServicePlatform':
            # 政府单位名
            self.site_name = '中国招标投标公共服务平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 	铜陵有色金属集团控股有限公司
        elif spider.name == 'TongLinYouSeMetal_oldPro':
            # 政府单位名
            self.site_name = '铜陵有色金属集团控股有限公司'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # 	阳光七采·兵纷招采—中国兵器电子招标投标交易平台
        elif spider.name == 'SunShineSevenMiningPro':
            # 政府单位名
            self.site_name = '阳光七采·兵纷招采—中国兵器电子招标投标交易平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://sc.tzxm.gov.cn/showinformation
        elif spider.name == 'SiChuanGovernmentservicePro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-四川省'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://nmg.tzxm.gov.cn/tzsp/projectHandlePublicity.jspx
        elif spider.name == 'NeiMengGuInvestPro':
            # 政府单位名
            self.site_name = '内蒙古自治区投资项目在线审批办事大厅'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # https://tzxm.shaanxi.gov.cn/tzxmspweb/phgs
        elif spider.name == 'ShanXiOnlineGovernPro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-陕西省'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)


        # https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2#this
        elif spider.name == 'ChinaYiDongInvestPro':
            # 政府单位名
            self.site_name = '中国移动采购与招标网'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://tzxm.hubei.gov.cn/tzxmweb/pages/home/approvalResult/recordqueryNew.jsp
        elif spider.name == 'HuBeiOnlineGovernPro':
            # 政府单位名
            self.site_name = '湖北省投资项目在线审批监管平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://www.qhtzxm.gov.cn/info/toListPage
        elif spider.name == 'QingHaiOnlineInvestPro':
            # 政府单位名
            self.site_name = '青海省投资项目在线审批监管平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)


        # https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html#
        elif spider.name == 'GuangDongOnlineInvestPro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-广东省'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # https://tzxm.drc.xizang.gov.cn:8008/report/publicInfo
        elif spider.name == 'XiZangOnlineInvestPro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-西藏自治区'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://tzxm.jxzwfww.gov.cn/icity/ipro/open/publicity
        elif spider.name == 'JiangXiOnlineInvestPro':
            # 政府单位名
            self.site_name = '江西省投资项目在线审批监管平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://ec.mcc.com.cn/logonAction.do
        elif spider.name == 'ChinaMinmetalsCorportionFivePlatformIndexHome':
            # 政府单位名
            self.site_name = '中国五矿集团有限公司采购电子商务平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://110.249.223.65:8070
        elif spider.name == 'HebeiProvinceEcologyEnvironmentPro':
            # 政府单位名
            self.site_name = '河北省生态环境厅行政许可网上审批平台'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)


        # http://ggzy.ah.gov.cn
        elif spider.name == 'AnHuiProvicePlatformPro':
            # 政府单位名
            self.site_name = '安徽省公共资源交易监管网'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # http://221.214.94.51:8081/icity/ipro/projectlist
        elif spider.name == 'ShanDongProvinceBiddingSupervisionPro':
            # 政府单位名
            self.site_name = '全国投资项目在线审批监管平台-山东省'
            # 栏目名
            self.title_type = '拟在建项目'
            #  # 调用API 并写入
            self.currency(item=item, spider=spider)

        # # 包钢电子采购交易平台 !!!!!! 暂时不要爬取
        # if spider.name == 'BaoGangElectronicPlatform':
        #     # 政府单位名
        #     self.site_name = '包钢电子采购交易平台'
        #     # 栏目名
        #     self.title_type = '拟在建项目'
        #     #  # 调用API 并写入
        #     self.currency(item=item, spider=spider)

    def currency(self, item, spider):
        # 调用spider 生成id 与key的方法
        logger.info(f"目前运行的文件为：{spider.name}")
        api = APIManager()
        sd = SpiderData()
        item['title_date'] = sd.getTitleDate(item['title_date'])

        data = {
            "title_date": item["title_date"],
            "title_name": item['title_name'],
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "site_name": self.site_name,
            "title_type": self.title_type,
            "title_url": item['title_url'],
            "title_source": self.site_name,
            "site_path_name": item['site_path_name'],
            "site_path_url": item['site_path_url'],
            "content_html": item['content_html'],
            "update_user": "lzc",
            'site_id': item["site_id"]
        }

        temp_title_data = {
            "title_name": item['title_name'],
            "title_url": item['title_url'],
            "site_name": self.site_name,
        }
        title_id = sd.getTitleID(temp_title_data)
        if data["title_type"] == '国家部委':
            req = httpx.get('http://mykyls.xyz:38080/api/spider_zfbw_data_detail/{}/'.format(title_id))

            if 200 <= req.status_code <= 300:
                ser = api.addDataToZfbwDB(data)  # 政府部委
                api.updateConfigZfbw(site_id=data['site_id'], run_user=data['update_user'])
                self.update_print(ser, data)
            else:
                ser = api.addDataToZfbwDB(data)  # 政府部委
                api.updateConfigZfbw(site_id=data['site_id'], run_user=data['update_user'])
                self.add_print(ser, data)
        elif data["title_type"] == '拟在建项目':
            req = httpx.get('http://mykyls.xyz:38080/api/spider_nzj_data_detail/{}/'.format(title_id))
            if 200 <= req.status_code <= 300:
                ser = api.addDataToNzjDB(data)  # 政府部委
                api.updateConfigNzj(site_id=data['site_id'], run_user=data['update_user'])
                self.update_print(ser, data)
            else:
                ser = api.addDataToNzjDB(data)  # 政府部委
                api.updateConfigNzj(site_id=data['site_id'], run_user=data['update_user'])
                self.add_print(ser, data)
        elif data["title_type"] == '矿山企业':
            req = httpx.get('http://mykyls.xyz:38080/api/spider_kscp_data_detail/{}/'.format(title_id))
            if 200 <= req.status_code <= 300:
                ser = api.addDataToKscpDB(data)  # 政府部委
                api.updateConfigKscp(site_id=data['site_id'], run_user=data['update_user'])
                self.update_print(ser, data)
            else:
                ser = api.addDataToKscpDB(data)  # 政府部委
                api.updateConfigKscp(site_id=data['site_id'], run_user=data['update_user'])
                self.add_print(ser, data)
        elif data["title_type"] == '新闻媒体':
            # 新闻媒体
            req = httpx.get('http://mykyls.xyz:38080/api/spider_news_data_detail/{}/'.format(title_id))
            if 200 <= req.status_code <= 300:
                ser = api.addDataToNewsDB(data)  # 政府部委
                api.updateConfigNews(site_id=data['site_id'], run_user=data['update_user'])
                self.update_print(ser, data)
            else:
                ser = api.addDataToNewsDB(data)  # 政府部委
                api.updateConfigNews(site_id=data['site_id'], run_user=data['update_user'])
                self.add_print(ser, data)
        else:
            # 临时数据表
            req = httpx.get('http://mykyls.xyz:38080/api/spider_temp_data_detail/{}/'.format(title_id))
            if 200 <= req.status_code <= 300:
                ser = api.addDataToTempDB(data)  # 临时数据表
                # api.updateConfigNews(site_id=data['site_id'], run_user=data['update_user'])
                self.update_print(ser, data)
            else:
                ser = api.addDataToTempDB(data)  # 政府部委
                # api.updateConfigNews(site_id=data['site_id'], run_user=data['update_user'])
                self.add_print(ser, data)

    def status(self, data, ser):
        if ser.__contains__(404):
            logger.error(f"{data['site_path_url']} | {data['site_path_url']} 网站错误")

    def update_print(self, ser, data):
        print("*" * 30)
        logger.warning(f"{data['title_name'], data['title_date'], data['title_url']}\n |{ser}>> 更新成功")

    def add_print(self, ser, data):
        print("*" * 30)
        logger.info(f"{data['title_name'], data['title_date'], data['title_url']}\n |{ser}>> 添加成功")
