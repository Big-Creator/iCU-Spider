#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-5-31

import lxml
import pymongo
import re
import datetime
import random
import randomhms
from bs4 import BeautifulSoup
import requests

# 艺术类招生章程,2012,2013年须从数据库取（网页没有内容）
class Spider():
    def __init__(self):
        self.url_list = [
            'http://zs.tjcu.edu.cn/info/1024/1184.htm',
            'http://zs.tjcu.edu.cn/info/1024/1183.htm',
            'http://zs.tjcu.edu.cn/info/1024/1185.htm',
            'http://zs.tjcu.edu.cn/info/1024/1181.htm',
            'http://zs.tjcu.edu.cn/info/1024/1179.htm'
        ]
    def tool(self, text):
        pattern = re.compile('<.*?>', re.S)
        text = re.sub(pattern, '', text)
        return text
    def getHtml(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        result = r.text
        return result
        # print result

    def getData(self):
        data = []
        for url in self.url_list:
            html = self.getHtml(url)
            title = re.findall(r'<h1 class="h2 g-color-black g-font-weight-400">(.*?)</h1>', html, re.S)
            info = {}
            info['title'] = title[0]
            # now = datetime.datetime.now()
            #定义了一个随机生成时间点的函数，导入后组合
            hour = randomhms.randomhms()
            time = '2018-04-23'+" "+hour
            # print time
            info['time'] = time
            info['tagid'] = "[\"002\"]"
            info['typeid'] = 2  # 艺术类招生简章
            content = re.findall(r'<div class="g-pl-20--lg">(.*?)<div class="g-pr-20--lg">', html, re.S)
            info['content'] = content[0]
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
        db = client['yslzsjz']
        test = db['yslzs']
        test.insert(data)
        print 'Success!'

if __name__ == '__main__':
    spider = Spider()
    spider.toMongoDB()
