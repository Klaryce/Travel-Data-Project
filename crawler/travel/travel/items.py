# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DigItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Notes(scrapy.Item):
    city = scrapy.Field()
    time = scrapy.Field()
    view = scrapy.Field()
    like = scrapy.Field()
    reply = scrapy.Field()
    note_url = scrapy.Field()

class Notes2(scrapy.Item):
    id = scrapy.Field()
    time = scrapy.Field()
    note_url = scrapy.Field()

class NotesContent(scrapy.Item):
    date = scrapy.Field()
    city = scrapy.Field()
    content = scrapy.Field()
    days = scrapy.Field()
    when = scrapy.Field()
    money = scrapy.Field()
    with_whom = scrapy.Field()
    entertainment = scrapy.Field()