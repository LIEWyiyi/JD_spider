# -*- coding: utf-8 -*-
'''
__author__ = 'KaNgai'
Crawl old JD comment
'''
from JD_spider.items import JdSpiderItem
import scrapy
from scrapy.http import Request
from scrapy import log
from scrapy.selector import Selector
import re

class JDspider(scrapy.Spider):
    name = 'JDspider'
    allowed_domains = ["club.jd.com"]
    start_urls = ["http://club.jd.com/review/10178500-1-2-0.html"]
    download_delay = 1

    def parse(self, response):
        items = []
# response.xpath('//div[@data-widget="tab-content" and @class="mc"]')
        for index, sel in enumerate(response.xpath('//div[@class="i-item"]')):
            item = JdSpiderItem()
            comment = sel.xpath('div[2]/text()').extract()
            item['comment'] = [c.encode('utf-8') for c in comment]
            date = sel.xpath('div[1]/span[2]/text()').extract()
            item['date'] = date
            rank = sel.xpath('div[1]/span[1]/@class').extract()
            item['rank'] = [rank[0][7].encode('utf-8')]
            use_ful_less = sel.xpath('div[3]/div[1]/a/@title').extract()
            item['useful'] = [uf.encode('utf-8') for uf in use_ful_less[0]]
            item['useless'] = [ul.encode('utf-8') for ul in use_ful_less[1]]

            # items.append(item)
            # log.msg("Appending item...",level='INFO')

        # log.msg("Append done.",level='INFO')
        yield items


        # 获取下一页评论的url
        urls = response.xpath('//*[@class="next"]/@href').extract()
        for url in urls:
            print url
            yield Request(url=url, callback=self.parse)





