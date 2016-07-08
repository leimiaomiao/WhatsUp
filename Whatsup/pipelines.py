# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import json
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class WhatsupPipeline(object):
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
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        item['image_paths'] = image_paths
        return item
