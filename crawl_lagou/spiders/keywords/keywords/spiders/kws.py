# -*- coding: utf-8 -*-
import scrapy
from collections import defaultdict
class KwsSpider(scrapy.Spider):
    name = 'kws'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    def parse(self, response):
        # 获取标签总体分类名
        keys = response.xpath("//*[@class='menu_main job_hopping']/div/h2/text()").extract()
        # 新建一个defaultdict类,需使用一个类型来初始化。解决dict不存在默认值的问题
        item = defaultdict(list)
        # 标签索引
        i = 1
        for key in keys:
            key = key.strip()
            # 获取所有标签
            key_tags = response.xpath("//*[@class='menu_box'][{}]/div[2]/dl/dd/a/text()".format(i)).extract()
            for key_tag in key_tags:
                item[key].append(key_tag)
            i += 1
        print(item.keys())
        yield item
