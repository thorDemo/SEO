# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JunshiNewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    img_url = scrapy.Field()
    tips = scrapy.Field()
    create_time = scrapy.Field()
    state = scrapy.Field()
    news_time = scrapy.Field()