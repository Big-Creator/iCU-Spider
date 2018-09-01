#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymongo
import re
import datetime
import random
import randomhms
import requests

# 本科招生章程
class Spider():
    def tool(self, text):
        pattern = re.compile('<.*?>', re.S)
        text = re.sub(pattern, '', text)
        return text
    def getHtml(self):
        r = requests.get('http://zs.tjcu.edu.cn/search.jsp?wbtreeid=1020&searchScope=0&currentnum=1&newskeycode2=5pmu6YCa5pys56eR5oub55Sf56ug56iL')
        result = r.text
        return result
        # print result

    def getData(self):
        html = self.getHtml()
        pattern = re.compile(ur'<article>.*?<a.*?href="(.*?)">(.*?)招生章...</a>.*?</i>(\d+)年(.*?)月(.*?)日.*?</article>', re.S)
        result = re.findall(pattern, html)
        # for i in result:
        #     print i
        data = []
        str = '-'
        for i in result:
            info = {}
            url = 'http://zs.tjcu.edu.cn/'+i[0]
            info['title'] = self.tool(i[1])+u'招生章程'
            tim = []
            tim.append(i[2])
            tim.append(i[3])
            tim.append(i[4])
            time = str.join(tim)
            # now = datetime.datetime.now()
            hour = randomhms.randomhms()
            time = time+" "+hour
            # print time
            info['time'] = time
            info['tagid'] = "[\"001\"]"
            info['typeid'] = 1 #普通本科招生章程
            r = requests.get(url)
            r.encoding = 'utf-8'
            html = r.text
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
        db = client['bkzszc']
        test = db['bkzs']
        test.insert(data)
        print 'Success!'

if __name__ == '__main__':
    spider = Spider()
    spider.toMongoDB()
