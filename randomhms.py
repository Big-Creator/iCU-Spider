#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-5-31

import random


def randomhms():
    start = '0:0:0'
    end = '23:59:59'

    sh,sm,ss = start.strip().split(':')
    s_second = int(sh)*3600 + int(sm)*60 + int(ss)
    eh,em,es = end.strip().split(':')
    e_second = int(eh) * 3600 + int(em) * 60 + int(es)

    rt = random.randrange(s_second,e_second)

    m,s = divmod(rt,60)
    h,m = divmod(m,60)
    hms =  "%02d:%02d:%02d" % (h, m, s)
    # print hms
    return hms

if __name__ == '__main__' :
    randomhms()



