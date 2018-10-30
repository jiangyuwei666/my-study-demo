# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from douban.settings import *

class DoubanPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
