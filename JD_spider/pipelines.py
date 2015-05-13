# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class JdSpiderPipeline(object):

    def __init__(self):
        self.file = codecs.open('JD_data.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))

        return item


class MongoDBPipeline(object):

    def __init__(self):
        self.server = 'localhost'
        self.port = 27017
        self.db = 'JD'

    def process_item(self, item, spider):
        self.col = 'g646197'
        connection = pymongo.Connection(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("JD comment was added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
