# -*- coding: utf-8 -*-

# Scrapy settings for JD_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'JD_spider'

SPIDER_MODULES = ['JD_spider.spiders']
NEWSPIDER_MODULE = 'JD_spider.spiders'

COOKIES_ENABLED = False
ITEM_PIPELINES = {
    'JD_spider.pipelines.JdSpiderPipeline':300,
    'JD_spider.pipelines.MongoDBPipeline':500
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'JD_spider (+http://www.yourdomain.com)'
