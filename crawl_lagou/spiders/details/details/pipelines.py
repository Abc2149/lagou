# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DetailsPipeline(object):
    def process_item(self, item, spider):
        return item



class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            db='lagouspider',
            charset='utf8',
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''
        insert into lagou (kd,city,companyFullName, companyLabelList,positionAdvantage,companySize,district,education,financeStage,positionName,jobNature,workYear,salary) 
        VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") 
        '''% (item['kd'],item['city'], item['companyFullName'], item['companyLabelList'],item['positionAdvantage'], item['companySize'],
      item['district'], item['education'],item['financeStage'], item['positionName'],item['jobNature'],item['workYear'],item['salary'])

        self.cur.execute(sql)
        self.conn.commit()
        return item