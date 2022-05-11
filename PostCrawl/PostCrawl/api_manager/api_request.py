#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
====================================================================
Project Name: mining script
File description:
Author: Liao Heng
Create Date: 2022-02-22
====================================================================
"""
import json
import requests
import time
import socket


class APIRequest(object):
    """
    Description: 处理API请求
    """
    def __init__(self, username='test', password='test.com'):
        self.user = {"username": username, "password": password }
        self.header = self.getHeader()
        self.local_ip = self.getLocalIP()

    def getLocalIP(self):
        try:
            ip = ""
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            s.close()

        return ip

    def getHeader(self):
        while True:
            try:
                token_url = 'http://mykyls.xyz:38080/api-token-auth/'
                req = requests.post(token_url, data=self.user)
                token = req.json().get("token", "")
                if 200 <= req.status_code < 300:
                    token = req.json().get("token", "")
                    header = {'Authorization': 'token %s' % token,
                              'Content-Type': 'application/json'}
                    # print("Token pass：", token)
                    return header
                else:
                    print("Token fail: %s, %s" % (req.status_code, str(req.json())))
            except Exception as e:
                print('Token error:', str(e))
            time.sleep(5)

    def get(self, url, params={}, timeout=10):
        if "192.168.2" in self.local_ip:
            url = url.replace("mykyls.xyz:38080", "192.168.2.31:38080")
        fail_count = 0
        while True:
            try:
                req = requests.get(url, params=params, headers=self.header, timeout=timeout)
                if 200 <= req.status_code < 300:
                    return req.status_code, req.json()
                else:
                    print("get fail(%s): " % fail_count, req.status_code, req.json())
                    if fail_count > 20:
                        return req.status_code, req.json()
            except Exception as e:
                print("get error(%s): %s , %s" % (fail_count, url, str(e)))
            fail_count += 1
            time.sleep(5)

    def delete(self, url, timeout=10):
        if "192.168.2" in self.local_ip:
            url = url.replace("mykyls.xyz:38080", "192.168.2.31:38080")
        try:
            req = requests.delete(url, headers=self.header, timeout=timeout)
            result = req.json()
            return req.status_code, result
        except Exception as e:
            print("delete error: %s , %s" % (url, str(e)))
            return 400, [str(e)]

    def post(self, url, data, timeout=10):
        if "192.168.2" in self.local_ip:
            url = url.replace("mykyls.xyz:38080", "192.168.2.31:38080")
        try:
            req = requests.post(url, data=json.dumps(data), headers=self.header, timeout=timeout)
            result = req.json()
            return req.status_code, result
        except Exception as e:
            print("post error: %s , %s" % (url, str(e)))
            return 400, [str(e)]

    def put(self, url, data):
        if "192.168.2" in self.local_ip:
            url = url.replace("mykyls.xyz:38080", "192.168.2.31:38080")
        try:

            req = requests.put(url, data=json.dumps(data), headers=self.header)
            result = req.json()
            return req.status_code, result
        except Exception as e:
            print("put error: %s , %s" % (url, str(e)))
            return 400, [str(e)]

    def test(self):
        url = "http://mykyls.xyz:38080/api/spider_nzj_config/"
        url_params = {
            "site_id": "D1D6A64E07",
        }
        data = self.get(url, url_params)
        # print(data)


if __name__ == "__main__":
    api = APIRequest()
    api.test()
