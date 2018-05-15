# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DetailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 技术标签
    kd = scrapy.Field()
    # 城市
    city =scrapy.Field()
    # 公司名称
    companyFullName =scrapy.Field()
    # 公司标签
    companyLabelList =scrapy.Field()
    # 职位诱惑
    positionAdvantage =scrapy.Field()
    # 公司规模
    companySize =scrapy.Field()
    # 城市所在区
    district =scrapy.Field()
    # 学历要求
    education =scrapy.Field()
    # # 公司发展
    financeStage =scrapy.Field()
    # 职位
    positionName =scrapy.Field()
    # 薪资
    salary =scrapy.Field()
    # 工作经验
    workYear =scrapy.Field()
    # 工作性质
    jobNature =scrapy.Field()

