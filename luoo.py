#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-03-21 14:33:30
# Project: luoo

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in xrange(1,805):
            self.crawl('http://www.luoo.net/music/'+str(i), callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        d=response.doc('.vol-tracklist');
        list = [];
        for i in d.items('li'):
            list.append(i('.trackname').text()+' '+i('.player-wrapper .artist').text())
        return {
            "title": response.doc('.vol-title').text(),
            "type": response.doc('.vol-tag-item').text(),
            "songs": list,
            "article": response.doc('.vol-desc').text(),
        }
