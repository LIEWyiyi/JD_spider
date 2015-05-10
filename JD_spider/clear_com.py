# -*- coding: utf-8 -*-
__author__ = 'KaNgai'
import pymongo
import re
import os
import jieba
'''
    目的: 清理评论数据（清理无用评论）
         获取属性（先分词，再删除程度词，再对剩下的词计数）
'''

conn = pymongo.Connection('localhost', 27017)
db = conn["JD"]
col = db["g646197"]
pattern = {
    'num' : r'\d+',
    'punctuation' : r'[+\-*~@#$%^&()_=,\.;\:\"\'!]+',
}
def clean_comment(pattern, col):
    comment = []
    for item in col.find({},{"comment":1}):
        com = item["comment"][0]
        clean_com = re.sub(pattern['punctuation'], "", com)
        clean_com = re.sub(pattern['num'], "", clean_com)
        len_clean_com = len(clean_com)
        if len_clean_com == 0:
            continue
        else:
            comment.append(com)
    return comment

def pick_most_dict(dir):
    most_dict = []
    most_dict_dir = os.listdir(dir)    # 获取程度词目录下文件列表
    for file in most_dict_dir:
        most_dict_file = open(os.path.join(dir, file),  mode = 'r').readlines()
        for dict in most_dict_file:
            most_dict.append(dict.replace('\n', ''))   # 去除换行符
    return most_dict

def clean_most_comment(cut_comment, most_dict):
    """
    :param cut_comment: 已经分词的评论，[['','',''],[],[],[]]
    :param most_dict: 程度词列表，['','','','']
    :return: clean_comment: 去除程度词的评论分词，['','','','']
    """
    clean_comment = []
    for com in cut_comment:
        for com_cut in com:
            if com_cut in most_dict:
                continue
            else:
                clean_comment.append(com_cut)
    return clean_comment

def cut_comment(comment):
    cut_comment = []
    for com in comment:
        cut_comment.append(list(jieba.cut(com)))
    return cut_comment

dir = "G:\Users\KaNgai\Documents\GitHub\JD_spider\JD_spider\sentiment"