# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Typical uses of item pipelines are:
# cleansing HTML data
# validating scraped data (checking that the items contain certain fields)
# checking for duplicates (and dropping them)
# storing the scraped item in a database

import scrapy
import json
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymongo


class MongoPipeline(object):
    collection_name = 'whatsup'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])


class JsonWriterPipeline(object):
    def __init__(self):
        self.urls_seen = set()
        self.file = open('./data/%s.json' % 'data', 'w')
        self.comma = ''

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
        line = self.comma + json.dumps(dict(item)) + "\n"
        self.comma = ','
        self.file.write(line)
        return item

    def open_spider(self, spider):
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')


class WhatsupImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item:
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['image_paths'] = image_paths
        return item
