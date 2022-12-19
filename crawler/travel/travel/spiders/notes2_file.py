# -*- coding: utf-8 -*-

import scrapy
import datetime
from travel.items import Notes2

i = 0

class NotesFileSpider(scrapy.Spider):
    name = "notes2_file"

    start_urls = [
        "https://you.ctrip.com/travels/china110000/t3.html",
    ]


    def parse(self, response):
        global i
        notes = response.css("a.journal-item.cf::attr(href)").getall()

        item = Notes2()
        time = datetime.date.today()
        for note in notes:
            yield{
                'id': i,
                'time': str(time),
                'note_url': "https://you.ctrip.com" + note
            }
            i += 1
        if(i < 30000):
            next_url = "https://you.ctrip.com" + response.css("a.nextpage::attr(href)").get()
            yield scrapy.Request(next_url, callback=self.parse)