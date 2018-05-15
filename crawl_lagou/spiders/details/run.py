from scrapy import cmdline

cmdline.execute('scrapy crawl dts --nolog'.split())
#暂停，恢复爬虫
# cmdline.execute('scrapy crawl dts -s JOBDIR=crawls/dts-1'.split())

# log
# scrapy crawl spider1 -L WARNING