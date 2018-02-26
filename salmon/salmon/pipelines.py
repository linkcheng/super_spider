# -*- coding: utf-8 -*-
from pymongo import MongoClient
from salmon.settings import MONGODB_CONFIG


class SalMonPipeline(object):
    def __init__(self):
        self.mongo_cli = MongoClient(MONGODB_CONFIG.get('uri'))
        self.mongo_db = self.mongo_cli[MONGODB_CONFIG.get('db')]
        self.salmon = self.mongo_db['salmon']

    def process_item(self, item, spider):
        self.upsert(item, spider)
        return item

    def upsert(self, item, spider):
        """插入数据库"""
        where = {
            'mobile': item['mobile'],
        }

        val = {
            '$set': {
                'mobile': item['mobile'],
                item['name']: {
                    'url': item['url'],
                    'msg': item['message'],
                    'ret': item['result'],
                },
            }
        }
        self.salmon.update(where, val, upsert=True)

    def close_spider(self, spider):
        pass
