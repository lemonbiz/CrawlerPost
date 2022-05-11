"""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 #
# @Time    : 2022/3/31 10:41
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : selenium_option.py
# @Software: PyCharm
"""
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def option_selenium(self):
    # 添加特殊配置
    options = webdriver.ChromeOptions()
    # 设置默认编码为 utf-8，也就是中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 模拟 android QQ浏览器
    # options.add_argument(
    #     'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
    # 禁止硬件加速
    options.add_argument('--disable-gpu')
    # 取消沙盒模式
    options.add_argument('--no-sandbox')
    # 禁止弹窗广告
    options.add_argument('--disable-popup-blocking')
    # 最大界面
    options.add_argument('--window-size=1920,1080')
    # 去掉反扒标志
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 此方法针对V78版本及以上有效，同时可以解决部分网站白屏的问题。
    options.add_experimental_option('useAutomationExtension', False)
    # # 大量渲染时候写入/tmp而非/dev/shm
    options.add_argument("-–disable-dev-shm-usage")
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    # 忽略证书错误 （实操没卵用）
    options.add_argument('--ignore-certificate-errors')
    # 真实浏览器
    self.bro = webdriver.Chrome(executable_path="../chrome/chromedriver.exe",chrome_options=options)

    self.bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                               Object.defineProperty(navigator, 'webdriver', {
                                 get: () => undefined
                               })
                             """
    })

