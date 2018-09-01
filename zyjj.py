#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-5-13

import requests
import re
import pymongo
import randomhms
from lxml import etree
# 专业简介

class Spider():
    def __init__(self):
        self.url = 'http://zs.tjcu.edu.cn/yxzy/jxgcxy.htm'
    def getHtml(self,url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        return html

    def getData(self):
        url_list = []
        data = []
        html = self.getHtml(self.url)
        xw_url_html = re.findall(ur'<ul.*?aria-labelledby="nav-link--1006".*?>(.*?)</ul>', html, re.S)
        xw_url = re.findall(ur'.*?<a class="nav-link" href="(.*?)">.*?学院</a>.*?', xw_url_html[0], re.S)
        for xw in xw_url:
            url = 'http://zs.tjcu.edu.cn/yxzy/' + xw
            url_list.append(url)
        for url in url_list:
            xw_html = self.getHtml(url)
            result = re.findall('<!-- Card -->(.*?)<!-- End Card -->', xw_html, re.S)
            pattern = re.compile(r'<span class="u-accordion__control-icon g-mr-10">.*?</span>(.*?)</a>', re.S)
            for j in result:
                info = {}
                info['time'] = '2018-04-23'+' '+randomhms.randomhms()
                title = re.findall(pattern, j)
                info['title'] = title[0]
                info['content'] = j
                info['tagid'] = "[\"005\"]"
                info['typeid'] = 5  # 专业简介
                data.append(info)
        return data

    def toServer(self):
        data = self.getData()
        for i in data:
            r = requests.post('https://icu.wangxuefeng.com.cn/article/post', data=i)
            print r.text
            break
        print 'End!'

    def toMongoDB(self):
        data = self.getData()
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['zyjj']
        test = db['zhuanyejianjie']
        test.insert(data)
        print 'Success!'

if __name__ == '__main__':
    spider = Spider()
    spider.toMongoDB()
