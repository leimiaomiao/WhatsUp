# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # title of the news
    title = scrapy.Field()

    # url of the original news
    url = scrapy.Field()

    # slug
    slug = scrapy.Field()

    # news body
    content = scrapy.Field()

    # image link within news body
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()

    # news audio
    audio = scrapy.Field()

    # date of the news
    date = scrapy.Field()
