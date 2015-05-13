# -*- coding: utf-8 -*-
'''
__author__ = 'KaNgai'
Crawl new JD comment
'''
from JD_spider.items import JdSpiderItem
import scrapy
from scrapy.http import Request
from scrapy import log
from scrapy.selector import Selector
import re

class JDcrawl(scrapy.Spider):
    name = 'JDcrawl'
    allowed_domains = ["club.jd.com"]
    start_num = [646197]
    # start_urls = ["http://club.jd.com/review/" + num + "-1-1-4.html" for num in start_num]
    start_urls = ["http://club.jd.com/review/646197-1-1-0.html"]
    download_delay = 1

    def parse(self, response):
        items = []
        goods = response.xpath('//li[@class="p-name"]')
        goods_num = goods.xpath('a/@href').extract()
        goods_num = re.findall(u'http://item.jd.com/(\d*).html', goods_num[0])
        goods_name = goods.xpath('a/text()').extract()
        goods_name = [g.encode('utf-8') for g in goods_name]

        for index, sel in enumerate(response.xpath('//div[@data-widget="tab-content" and @class="mc"]')):
            item = JdSpiderItem()
            item['goods_num'] = goods_num[0]
            item['goods_name'] = goods_name

            comment_tags = sel.xpath('div[1]/div[2]/div[2]/dl')

            if len(comment_tags) == 1:
                comment = comment_tags[0].xpath('dd/text()').extract()
                item['comment'] = [c.encode('utf-8') for c in comment]
                item['tags'] = []
            else:
                comment_tags_1 = comment_tags[0].xpath('dt/text()').extract()
                if comment_tags_1[0][0] == u'\u5fc3':       # 匹配心得
                    comment = comment_tags[0].xpath('dd/text()').extract()
                    item['comment'] = [c.encode('utf-8') for c in comment]
                    item['tags'] = []

                if comment_tags_1[0][0] == u'\u6807':       # 匹配标签
                    tags =comment_tags[0].xpath('dd/span/span/text()').extract()
                    item['tags'] = [t.encode('utf-8') for t in tags]
                    comment = comment_tags[1].xpath('dd/text()').extract()
                    item['comment'] = [c.encode('utf-8') for c in comment]

            rank = sel.xpath('div[1]/div[2]/div[1]/span[1]/@class').extract()
            item['rank'] = rank[0][7].encode('utf-8')
            useful = sel.xpath('div[1]/div[2]/div[3]/div[1]/a/@title').extract()
            item['useful'] = useful[0]

            buydate = sel.xpath('div[1]/div[2]/div[2]/div/dl')
            if len(buydate)==2:
                buy_date = buydate[1].xpath('dd/text()').extract()
                item['buy_date'] = buy_date[0].replace("\r\n","")
            else:
                buy_date = buydate.xpath('dd/text()').extract()
                item['buy_date'] = buy_date[0].replace("\r\n","")

            comment_date = sel.xpath('div[1]/div[2]/div[1]/span[2]/a/text()').extract()
            item['comment_date'] = comment_date[0].replace("\r\n","")
            yield item

            # items.append(item)
            # log.msg("Appending item...",level='INFO')

        # log.msg("Append done.",level='INFO')
        # return items


        # 获取下一页评论的url
        urls = response.xpath('//*[@class="next"]/@href').extract()
        for url in urls:
            print url
            yield Request(url=url, callback=self.parse)






