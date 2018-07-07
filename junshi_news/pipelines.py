# -*- coding: utf-8 -*-
import pymysql
from junshi_news.DBtools.dbhelper import DBHelper
from junshi_news.items import JunshiNewsItem


class JunshiNewsPipeline(object):

    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        if isinstance(item, JunshiNewsItem):
            sql = 'insert into junshi_news(title, content, img_url, tips, news_time) VALUES (%s,%s,%s,%s,%s)'
            print('插入新闻')
            parm = (item['title'], item['content'], item['img_url'], item['tips'], item['news_time'])
            self.db.insert(sql, parm)
            return item
