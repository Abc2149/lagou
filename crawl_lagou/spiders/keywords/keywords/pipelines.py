# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, os, codecs

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class KeywordsPipeline(object):
    def process_item(self, item, spider):
        return item


class SaveJsonPipeline(object):

    def __init__(self):
        self.file = codecs.open((basedir + '\json\keywords.json').replace('\\','/'), 'wb' ,encoding='utf-8')

    def process_item(self, item, spider):
        # json.dumps()序列化数据使用ascii编码，参数禁用ASCII编码，按utf-8编码。
        line = json.dumps(item,ensure_ascii=False)
        self.file.write(line)
        return item
