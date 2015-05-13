# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiderItem(scrapy.Item):

    goods_num = scrapy.Field()
    goods_name = scrapy.Field()
    comment = scrapy.Field()
    comment_date = scrapy.Field()
    buy_date = scrapy.Field()
    rank = scrapy.Field()
    tags = scrapy.Field()
    useful = scrapy.Field()
