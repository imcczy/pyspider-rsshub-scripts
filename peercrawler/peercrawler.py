#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-02 08:55:46
# Project: mteam

from pyspider.libs.base_handler import *
import random
from decoding import Decoder
from torrent import Torrent
import requests


class Handler(BaseHandler):
   
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            "Host": "tp.m-team.cc",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8,zh;q=0.6,zh-TW;q=0.4,zh-CN;q=0.2",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "DNT": "1",
            "Connection": "keep-alive"
        },

        'cookies': {
            "tp": "your m-team cookie"
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://tp.m-team.cc/adult.php', callback=self.index_page)

    @config(age=1 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="https://tp.m-team.cc/download"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        #with open(re.findall("\d{2,}",response.url)[0]+".torrent","wb") as torrent:
        #    torrent.write(response.content)
        #return {
        #    "url": response.url,
        #   "title": response.doc('title').text(),
        #}

        torrent = Torrent(response.content)
        peer_id = _calculate_peer_id()
        playload = {
            'info_hash': torrent.info_hash,
            'peer_id': peer_id,
            'port': 51413,
            'uploaded': 0,
            'downloaded': 0,
            'left': torrent.total_size,
            'compact': 1,
            'event': 'started'}
        url = 'http://ipv6.tp.m-team.cc/announce.php?passkey=5b4c5cd6afcdf9643176890ebad772ba'
        s = requests.session()
        s.headers.update({'User-Agent': 'Transmission/1.32 (6455)'})
        resp = s.get(url,params=playload)
        d = (Decoder(resp.content).decode())
        ip = []
        if d[b'peers'] is not None:
            for i in d[b'peers']:
                ip.append(i[b'ip'].decode())
        return{
            'ip': ip
        }

            

        
def _calculate_peer_id():
    """
    Calculate and return a unique Peer ID.

    The `peer id` is a 20 byte long identifier. This implementation use the
    Azureus style `-PC1000-<random-characters>`.

    Read more:
        https://wiki.theory.org/BitTorrentSpecification#peer_id
    """
    return '-TR1320-' + ''.join(
        [str(random.randint(0, 9)) for _ in range(12)])