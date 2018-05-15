# -*- coding: utf-8 -*-
import scrapy, json, os
from details.items import DetailsItem
import time


class DtsSpider(scrapy.Spider):
    name = 'dts'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    def __init__(self):
        super(DtsSpider, self).__init__()

        # 获取json文件中的标签数据
        self.basedir = 'D:/Desktop/python爬虫/crawl_lagou/json/keywords.json'
        # 注意load 与 loads 的区别
        self.keywords = json.load(open(self.basedir, encoding='utf-8'))
        self.referer = 'https://www.lagou.com/jobs/list_{}?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.kd_num = -2
        self.keywords_len = len(self.keywords['技术'])

    def start_requests(self):
        kd = self.keywords['技术'][self.kd_num]
        print(self.referer.format(kd))
        yield scrapy.FormRequest(url=self.url, formdata={'pn': '1', 'kd': kd}, method='POST',
                                 headers={'Referer': self.referer.format(kd)}, meta={'page': 1, 'kd': kd},
                                 dont_filter=True,
                                 callback=self.parse)

    def parse(self, response):
        # 可能返回的不是json数据
        try:
            data = json.loads(response.text)
        except ValueError:
            yield scrapy.FormRequest(url=self.url,
                                     formdata={'pn': str(response.meta.get('page')), 'kd': response.meta.get('kd')},
                                     method='POST', headers={'Referer': self.referer.format(response.meta.get('kd'))},
                                     meta={'page': response.meta.get('page'), 'kd': response.meta.get('kd')},
                                     dont_filter=True,
                                     callback=self.parse)
        try:
            # 判断当前是否有内容
            if data.get('content').get('positionResult').get('resultSize') != 0:
                results = data.get('content').get('positionResult').get('result')
                totalCount = data.get('content').get('positionResult').get('totalCount')
                for result in results:
                    item = DetailsItem()
                    # 职位
                    item['kd'] = response.meta.get('kd')
                    # 城市
                    item['city'] = result.get('city')
                    # 公司名称
                    item['companyFullName'] = result.get('companyFullName')
                    # 公司标签
                    if isinstance(result.get('companyLabelList'), list):
                        item['companyLabelList'] = ','.join(result.get('companyLabelList'))
                    else:
                        item['companyLabelList'] = ''
                    # 公司规模
                    item['companySize'] = result['companySize']
                    # 城市所在区
                    item['district'] = result['district']
                    # 学历
                    item['education'] = result['education']
                    # 公司发展
                    item['financeStage'] = result['financeStage']
                    # 工作性质
                    item['jobNature'] = result['jobNature']
                    # 职位诱惑
                    item['positionAdvantage'] = result['positionAdvantage']
                    # 应聘职位
                    item['positionName'] = result['positionName']
                    # 薪资
                    item['salary'] = result['salary']
                    # 工作经验
                    item['workYear'] = result['workYear']
                    yield item

                all_page = int(totalCount / 15) + 1
                if all_page > 31:
                    all_page = 30
                    page = response.meta.get('page') + 1
                    if response.meta.get('page') < 30:
                        print('请求职位----->%s 第%s页'% (response.meta.get('kd'), page))
                        # time.sleep(5)
                        kd = response.meta.get('kd')
                        yield scrapy.FormRequest(url=self.url,
                                                 formdata={'pn': str(page), 'kd': kd},
                                                 method='POST', headers={'Referer': self.referer.format(kd)},
                                                 meta={'page': page, 'kd': kd},
                                                 dont_filter=True,
                                                 callback=self.parse)

                    if all_page == response.meta.get('page'):
                        self.kd_num += 1
                        if self.kd_num < self.keywords_len:
                            kd = self.keywords['技术'][self.kd_num]
                            print('请求职位----->', kd)
                            time.sleep(25)
                            yield scrapy.FormRequest(url=self.url, formdata={'pn': '1', 'kd': kd}, method='POST',
                                                     headers={'Referer': self.referer.format(kd)},
                                                     meta={'page': 1, 'kd': kd},
                                                     dont_filter=True,
                                                     callback=self.parse)

                else:
                    page = response.meta.get('page') + 1
                    if response.meta.get('page') < all_page:
                        print('请求职位----->%s 第%s页'% (response.meta.get('kd'), page))
                        # time.sleep(5)
                        kd = response.meta.get('kd')
                        yield scrapy.FormRequest(url=self.url,
                                                 formdata={'pn': str(page), 'kd': kd},
                                                 method='POST', headers={'Referer': self.referer.format(kd)},
                                                 meta={'page': page, 'kd': kd},
                                                 dont_filter=True,
                                                 callback=self.parse)
                    # 所有页面爬取完毕，取下一个标签。
                    if all_page == response.meta.get('page'):
                        self.kd_num += 1
                        if self.kd_num < self.keywords_len:
                            kd = self.keywords['技术'][self.kd_num]
                            print('请求职位----->', kd)
                            time.sleep(25)
                            yield scrapy.FormRequest(url=self.url, formdata={'pn': '1', 'kd': kd}, method='POST',
                                                     headers={'Referer': self.referer.format(kd)},
                                                     meta={'page': 1, 'kd': kd},
                                                     dont_filter=True,
                                                     callback=self.parse)
            else:
                self.kd_num += 1
                if self.kd_num < self.keywords_len:
                    kd = self.keywords['技术'][self.kd_num]
                    print('请求职位----->', kd)
                    time.sleep(25)
                    yield scrapy.FormRequest(url=self.url, formdata={'pn': '1', 'kd': kd}, method='POST',
                                             headers={'Referer': self.referer.format(kd)},
                                             meta={'page': 1, 'kd': kd},
                                             dont_filter=True,
                                             callback=self.parse)

        except AttributeError:
            page = int(response.meta.get('page'))
            print('重试请求职位----->%s 第%s页'% (response.meta.get('kd'), page))
            time.sleep(30)
            kd = response.meta.get('kd')
            yield scrapy.FormRequest(url=self.url,
                                     formdata={'pn': str(page), 'kd': kd},
                                     method='POST', headers={'Referer': self.referer.format(kd)},
                                     meta={'page': page, 'kd': kd},
                                     dont_filter=True,
                                     callback=self.parse)



