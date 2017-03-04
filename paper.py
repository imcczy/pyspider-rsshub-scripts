#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-07 08:33:16
# Project: paper

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690850', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://dblp.uni-trier.de/db/conf"]').items():
            self.crawl(each.attr.href, callback=self.conf_page)

    
    @config(priority=2)
    def conf_page(self, response):
        i = 0
        for each in response.doc('a[href^="http://dblp.uni-trier.de/db/conf"]').items():
            match = re.search('\d{4}',each.attr.href)
            if match:
                if int(match.group()) >= 2011:
                    self.crawl(each.attr.href, callback=self.detail_page)
            else:
                continue
    
    def detail_page(self, response):
        paper = [];
        for each in response.doc('ul.publ-list > li').items():
            papertitle = each('.title').text();
            if papertitle.find('droid') > -1:
                paper.append(papertitle)
        return{
            'title': paper
        }
