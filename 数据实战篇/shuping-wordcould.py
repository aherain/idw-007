#!/usr/bin/python3
# coding: utf-8

import pymysql
from urllib import parse
import json
import time
import requests
import re
import jieba
import jieba.analyse
import csv
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

Mac_headers = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}

class SWD(object):

    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "pass147_", "zhihu")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute("SELECT VERSION()")

    def db_insert(self,fields,  datas):
        sql = '''INSERT INTO lvpishu(%s) VALUES (%s) ''' % (fields, datas)

        try:
            # 执行sql语句
            print(sql)
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            pass
            # 发生错误时回滚
            self.db.rollback()
        return 1

    def db_close(self):
        self.cursor.close()

    def scrapy_url_words(self):
        print("抓取豆瓣主题词")
        urll = "https://movie.douban.com/subject/27060077/comments?start=%s&limit=20&sort=new_score&status=P&percent_type=h"
        URL_list = [urll % page for page in range(220, 480, 20)]
        for url in URL_list:
            time.sleep(3)
            wb_data = requests.get(url, headers=Mac_headers)
            soup = BeautifulSoup(wb_data.text,  'html.parser')
            bb = soup.find_all("div", class_="comment-item")
            for line in bb:
                a=line.select('.votes')[0].string
                b=line.select('.short')[0].string
                fields = 'content, votes'
                datas = "'%s',%s " % (str(b).replace('\'',''), a)
                self.db_insert(fields, datas)
        self.db_close()

    def insert_words(self, dd, w_id):
        sql = """update lvpishu set key_words='%s', status=1 where id=%s""" % (','.join(dd), w_id)
        print(sql)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:

            self.db.rollback()
            raise
        return 1

    def jieba_key_words(self):
        sql = "SELECT id, content FROM lvpishu where status=0"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                w_id = row[0]
                content = row[1]
                # 基于TextRank算法进行关键词抽取
                textrank = jieba.analyse.textrank
                keywords_TR = textrank(content, topK=15, withWeight=False, allowPOS=('a','ad','an','tg','t','s','nr','ns','nz','an','ns', 'n', 'q', 'vn'))
                print('textrank抽取的关键词：\n', keywords_TR)
                self.insert_words(keywords_TR, w_id)
                print('保存成功')

        except:
            raise

    def getccw(self):
        sql = '''SELECT key_words FROM zhihu.lvpishu'''
        cloud_text = ' '
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for row in results:
            if not row[0]:
                continue
            a =  [r for r in row[0].split(',') if '结局' not in r and '小说' not in r and '原著' not in r and '团圆' not in r ]
            cloud_text = cloud_text+ ','.join(a)
        return cloud_text

    def make_cloud(self):
        from wordcloud import WordCloud
        cloud_text = self.getccw()
        wc = WordCloud(
            # mask=alice_mask,
            background_color="white", #背景颜色
            max_words=500, #显示最大词数
            font_path="simhei.ttf",  #使用字体
            min_font_size=3,
            max_font_size=60,
            height=800,
            width=1024, #图幅宽度
            )
        wc.generate(cloud_text)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        wc.to_file("aa.png")

if __name__ == "__main__":
    print("开始抓取")
    swd = SWD()
    swd.scrapy_url_words()
    swd.jieba_key_words()
    swd.make_cloud()
