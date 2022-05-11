"""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 #
# @Time    : 2021/12/30 13:42
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : context.py
# @Software: PyCharm
"""
from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

class CustomContextFactory(ScrapyClientContextFactory):
    """
    Custom context factory that allows SSL negotiation.
    """

    # def __init__(self):
        # super(CustomContextFactory, self).__init__()
        # Use SSLv23_METHOD so we can use protocol negotiation
    _ssl_method = SSL.SSLv2_METHOD
