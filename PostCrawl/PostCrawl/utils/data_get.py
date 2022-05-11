"""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 #
# @Time    : 2022/4/8 13:35
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : data_get.py
# @Software: PyCharm
"""
from copy import deepcopy

import scrapy
from scrapy.http import JsonRequest




class GetData(object):

    def data_get(self,response):
        # 调用item
        item = {}
        item['site_path_url'] = response.meta.get("site_path_url")
        item['site_id'] = response.meta.get("site_id")
        item['site_path_name'] = response.meta.get("site_path_name")
        return item


class HandleRequest(object):
    def Json(self, callback, url_list, site_path_url, data=None):
        for url in url_list:
            yield JsonRequest(
                url=url,
                data=data,
                callback=callback,
                meta={
                    "site_path_url": deepcopy(site_path_url)
                }
            )

    def Get(self, callback, url_list, site_path_url):
        for url in url_list:
            yield scrapy.Request(
                url=url,
                callback=callback,
                meta={
                    "site_path_url": deepcopy(site_path_url)
                }
            )