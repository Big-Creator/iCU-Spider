#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-3

import pymongo
import requests
import re
import randomhms

# 天商印象
class Spider():
    def getHtml(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        return html

    def getData(self):
        data = []
        info = {}
        html = self.getHtml('http://zs.tjcu.edu.cn/zjts/tsyx.htm')
        info['title'] = '天商印象'
        info['time'] = '2018-5-20 '+randomhms.randomhms()
        content = re.findall(r'<div class="g-pl-10">(.*?)<div class="g-pr-20--lg">', html, re.S)
        jpgsrc = re.compile('/__local')
        content[0] = re.sub(jpgsrc, 'http://zs.tjcu.edu.cn/__local', content[0])
        info['content'] = content[0]
        info['tagid'] = "[\"018\"]"
        info['typeid'] = 7  # 天商印象（图片）
        data.append(info)
        return data

    def toServer(self):
        data = self.getData()
        r = requests.post('https://icu.wangxuefeng.com.cn/article/post', data=data)
        print r.text
        print 'End!'

    def toMongoDB(self):
        data = self.getData()
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['tsyx']
        test = db['tianshangyinxiang']
        test.insert(data)
        print 'Success!'

if __name__ == '__main__':
    spider = Spider()
    spider.toMongoDB()
