# -*- coding: utf-8 -*-
__author__ = 'KaNgai'
import pymongo
import jieba
import jieba.posseg as pseg
import jieba.analyse
conn = pymongo.Connection('localhost', 27017)
db = conn["JD"]
col = db["g646197"]
# 提取标签
tags = []
for item in col.find({},{"tags":1}):
    temp = item['tags']
    if temp:
        for t in range(len(temp)):
            tags.append(temp[t])

tags_n = {}
for t in tags:
    words = pseg.cut(t)
    for w in words:
        if w.flag == 'n':
            if w.word in tags_n:
                tags_n[w.word] += 1
            else:
                tags_n[w.word] = 1
# 提取评论
comment = []
com_keywords = []
for item in col.find({},{"comment":1}):
    temp = item['comment'][0]
    print temp
    words = list(jieba.cut(temp))
    try:
        a1 = jieba.analyse.textrank(temp)
        aa=''
        for a in range(len(a1)):
            aa = aa + a1[a] + '/'
        print aa
    except:
        print 'This comment have no keywords'
        aa = 'None'
    if temp:
        comment.append(temp)
        com_keywords.append(aa)




