#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-04-18 17:26:44
# Project: wooyun

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in xrange(1,1901):
            self.crawl('http://www.wooyun.org/bugs/new_public/page/'+str(i), callback=self.index_page)
            
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('td > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('.wybug_title').text(),
        }
