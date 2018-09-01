#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-5-13

import pymongo
import requests
import re
import randomhms

# 历年分数线一览表
class Spider():
    def __init__(self):
        self.url_list = [
            'http://zs.tjcu.edu.cn/bkzn/lnfs.htm',
            'http://zs.tjcu.edu.cn/bkzn/lnfs/1.htm',
            'http://zs.tjcu.edu.cn/bkzn/lnfs/2.htm',
            'http://zs.tjcu.edu.cn/bkzn/lnfs/3.htm'
        ]
    def getHtml(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        return html

    def getData(self):
        #共20+11 = 31条
        data = []
        for url in self.url_list:
            html = self.getHtml(url)
            # http://zs.tjcu.edu.cn/info/1022/1570.htm
            pattern = re.compile(r'<!-- Events Item -->.*?<h3.*?>(.*?)</h3>.*?<a.*?href=".*?info(.*?)"></a>.*?<!-- End Events Item -->', re.S)
            result1 = re.findall(pattern, html)
            # print len(result1)
            for j in result1:
                info1 = {}
                info1['title'] = j[0]
                info1['time'] = '2018-06-28 ' + '12:05:38'
                # print info1['time']
                ylbhtml = self.getHtml('http://zs.tjcu.edu.cn/info'+j[1])
                content = re.findall('<div class="g-pl-20--lg">(.*?)<div class="g-pr-20--lg">', ylbhtml, re.S)
                #通过正则将图片前加上链接
                jpgsrc = re.compile('/__local')
                content[0] = re.sub(jpgsrc, 'http://zs.tjcu.edu.cn/__local', content[0])
                info1['content'] = content[0]
                info1['tagid'] = "[\"003\"]"
                info1['typeid'] = 3  # 天津商业大学2015-2017年XXX录取情况一览表
                if info1 not in data:
                    data.append(info1)
        # print data
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
        db = client['lnfsxylb']
        test = db['lqqkylb']
        test.insert(data)
        print 'Success!'

if __name__ == '__main__':
    spider = Spider()
    spider.toMongoDB()
