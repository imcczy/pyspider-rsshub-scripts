#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-04-12 08:29:01
# Project: Android_APP

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for index in xrange(1,11):
            self.crawl('http://app.mi.com/catTopList/1?page='+str(index), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://app.mi.com/detail/"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "download_url": response.doc('.app-info-down > a').attr.href,
            "title": response.doc('.intro-titles > h3').text()
        }