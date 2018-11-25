#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-09 00:26:38
# Project: radioluoo

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(1,101):
            self.crawl('http://www.luoo.net/tag/?p='+str(i), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.vol-list > div.item > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        
        aespl = re.search('(?<=var\spl\s\=\s").*(?=")',response.text).group()
        tracks = dict()
        for each in response.doc('ul > li.track-item').items():
            tracks[each('.trackname').text()] = each('.artist').text()
        
        return {
            "num": response.doc('.vol-name > .vol-number').text(),
            "tags": response.doc('.vol-tag-item').text(),
            "desc": response.doc('.vol-desc').text(),
            "url": response.url,
            "title": response.doc('title').text(),
            "tracks": tracks,
            "aes":aespl
        }
