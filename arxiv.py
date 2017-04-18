#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-04-04 14:02:28
# Project: arxiv

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://arxiv.org/list/cs.CR/pastweek?skip=0&show=10', callback=self.index_page)

    #@config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('dl').items():
            for each_today in each('.list-identifier > a').items():
                if each_today.attr.href.find('abs') != -1:
                    self.crawl(each_today.attr.href, callback=self.detail_page)
            break
        #for each in response.doc('.list-identifier > a').items():
            #if each.attr.href.find('abs') != -1:
                #self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.title').text()
        authors = []
        for each in response.doc('.authors > a').items():
            authors.append(each.text())
        abstract = response.doc('.abstract').text()
        return {
            "url": response.url,
            "title": title,
        }
