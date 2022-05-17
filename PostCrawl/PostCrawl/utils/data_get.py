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

    def site_dict(self, site_path_url, site_path_name, site_id) -> dict:

        return {
            "site_path_url": deepcopy(site_path_url),
            "site_path_name": deepcopy(site_path_name),

            "site_id": deepcopy(site_id),
        }

    def data_get(self, response):
        # 调用item
        item = {}
        item['site_path_url'] = response.meta.get("site_path_url")
        item['site_id'] = response.meta.get("site_id")
        item['site_path_name'] = response.meta.get("site_path_name")
        return item

    def crawler_run(self):
        import sys
        import os
        from scrapy import cmdline
        file_name = os.path.basename(sys.argv[0])
        file_name = file_name.split(".")[0]
        cmdline.execute(['scrapy', 'crawl', file_name])


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
