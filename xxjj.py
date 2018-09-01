#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-3

import pymongo
import requests
import re
import pymysql
import json
import randomhms

# 学校简介
class Spider():
    def getHtml(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        return html

    def getData(self):
        data = []
        info = {}
        html = self.getHtml('http://zs.tjcu.edu.cn/zjts/tsjj.htm')
        info['title'] = u'天商简介'
        info['time'] = '2018-6-1 '+randomhms.randomhms()
        content = re.findall(r'<div class="g-pl-10">(.*?)<div class="g-pr-20--lg">', html, re.S)
        info['content'] = content[0]
        info['tagid'] = "[\"017\"]"
        info['typeid'] = 6  # 学校简介
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
        db = client['xxjj']
        test = db['xuexiaojianjie']
        test.insert(data)
        print 'Success!'

    # def toMysql(self):
    #     data = self.getData()
    #     #建立python与MySQL之间的连接
    #     mysql = pymysql.connect(host="localhost",user="root",passwd="12138",db="json",charset="utf8")
    #     #新建游标
    #     cur = mysql.cursor()
    #     #原生sql语句，创建一个名为jsondata的表，并在其中定义字段
    #     sqlc = """
    #         create table if not exists jsondata(
    #         typeid int(11) not null auto_increment primary key,
    #         tagid varchar(20) not null,
    #         title varchar(100) not null,
    #         time varchar(20) not null,
    #         content mediumtext not null)DEFAULT CHARSET=utf8;
    #      """
    #     cur.execute(sqlc)
    #     mysql.commit()
    #     print 'success'
    #     sqla = """
    #         insert into jsondata(typeid,tagid,title,time,content)values(%s,%s,%s,%s,%s);
    #     """
    #     #这里的data数据为列表，data[0]中存在的字典类型数据
    #     cur.execute(sqla, (data[0]['typeid'], data[0]['tagid'], data[0]['title'], data[0]['time'], data[0]['content']))
    #     mysql.commit()
    #     cur.close()
    #     mysql.close()
    #     print 'success'

if __name__ == '__main__':
    spider = Spider()
    spider.toMongoDB()

