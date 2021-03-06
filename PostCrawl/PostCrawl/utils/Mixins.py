"""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 #
# @Time    : 2022/4/2 10:39
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : Mixins.py
# @Software: PyCharm
"""

class Mixins(object):

    @staticmethod
    # 仅支持 Js 时间戳
    def time_format(time_num: int):
        import time
        timeStamp = int(time_num) / 1000
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

        return otherStyleTime

    @staticmethod
    # s为key不带双引号的json数据
    def jsonfy(s: str) -> object:
        # 此函数将不带双引号的json的key标准化
        obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
        return obj

    @staticmethod
    def IsContains(text, strings) -> bool:
        """
        :param strings:  被包含的值
        :param text:     原值
        :return: 返回的是一个布尔值
        """
        try:
            if isinstance(strings, str):
                if strings.find(text):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"意外中断……{e}")

    def cookies_dict(self, temp: str) -> dict:
        temp_list = temp.split('; ')
        # print(temp_list)

        # 创建空字典
        cookies = {}

        # 遍历列表
        for data in temp_list:
            key = data.split('=', 1)[0]  # (以'='切割，1为切割1次)
            value = data.split('=', 1)[1]
            cookies[key] = value
        return cookies

    @staticmethod
    def getTitleDate(page_str: str):
        """
        没有日的 自动变成每月的一号
        没有时间的 自动转换为当前时间
        超出当前时间30天的 自动转换为当前时间
        """
        # 获取日期
        # title_tag_str = "2021-06-03"
        # title_tag_str = "2021年06月03日"
        # title_tag_str = "2021/06/03"
        import datetime
        import re
        import time
        date_str = ""
        # 正则匹配如下
        re_str_list = [r"(20\d{2}[-年/.]\d+[-月/.]\d{2})",
                       r"(20\d{2}[-年/.]\d+[-月/.]\d{1})",
                       r"(20\d{2}-[01][0-9]--[0-3][0-9])",
                       r"(20\d{2}[-年/.]\d+[-月/.])",
                       ]

        # 遍历正则列表
        for re_str in re_str_list:
            temp_date_list = re.findall(re_str, page_str)
            # 如果匹配到
            if temp_date_list:
                # 直接赋值给 然后跳出循环
                date_str = temp_date_list[0]
                break

        #  如果匹配不到
        if date_str == "":
            # 然后再匹配
            re_str = "[^0-9]([0-3][0-9])(20\\d{2}-[01][0-9])"
            temp_date_list = re.findall(re_str, page_str)
            if temp_date_list:
                temp_list = list(temp_date_list[0])
                if len(temp_list) == 2:
                    date_str = "%s-%s" % (temp_list[1], temp_list[0])
        #  把年月日 -- / . 统统转换为-
        date_str = date_str.replace("年", "-").replace("月", "-").replace("日", "") \
            .replace("--", "-").replace("/", "-").replace(".", "-")
        temp_list = date_str.split("-")

        # 如果长度大于3
        if len(temp_list) == 3:
            # print(temp_list)
            # 如果第二个匹配项 例如 2022-1-1
            # 这个1 就要加个0
            if len(temp_list[1]) == 1:
                temp_list[1] = "0" + temp_list[1]
            # 同理
            if len(temp_list[2]) == 1:
                temp_list[2] = "0" + temp_list[2]

        date_str = "-".join(temp_list)
        # 获取当前时间
        now = datetime.datetime.now()
        # 在获取超过当前时间30天的时间
        delta = datetime.timedelta(days=30)
        n_days = now + delta
        # 格式化
        after_date = n_days.strftime('%Y-%m-%d')
        # 存在 且时间 在30天内 返回这个时间
        if date_str and date_str <= after_date:
            return date_str
        else:
            return time.strftime('%Y-%m-%d')

    @staticmethod
    def Get_domain_name(url, title_url):
        """
        :param url: 传入的网站
        :param title_url: 获取到链接地址
        :return:返回域名
        """
        # 如果开头以http的 则直接返回 title_url
        if title_url.startswith('http'):
            # 返回详情页url
            return title_url
        # 如果开头是 '/' 切割 传入的网址  转换为域名
        elif title_url.startswith('/'):
            dns_url = '/'.join(str(url).split('/')[:3])
            # 返回详情页url
            return dns_url + title_url
        # 如果开头是 './' 切割 传入的网址  转换为域名
        elif title_url.startswith('./'):
            dns_url = '/'.join(str(url).split('/')[:-1]) + '/'
            # 返回详情页url
            title_url = title_url.replace('./', '')
            return dns_url + title_url
        # 如果开头是 '../../../' 切割 传入的网址  转换为域名
        elif title_url.startswith('../../../'):
            dns_url = '/'.join(str(url).split('/')[:-4]) + '/'
            title_url = title_url.replace('../../../', '')
            # 返回详情页url
            return dns_url + title_url
        # 如果开头是 '../../' 切割 传入的网址  转换为域名
        elif title_url.startswith('../../'):
            dns_url = '/'.join(str(url).split('/')[:-3]) + '/'
            title_url = title_url.replace('../../', '')
            # 返回详情页url
            return dns_url + title_url
        # 如果开头是 '../' 切割 传入的网址  转换为域名
        elif title_url.startswith('../'):
            dns_url = '/'.join(str(url).split('/')[:-2]) + '/'
            title_url = title_url.replace('../', '')
            # 返回详情页url
            return dns_url + title_url
        else:
            dns_url = '/'.join(str(url).split('/')[:-1])
            return dns_url + title_url


