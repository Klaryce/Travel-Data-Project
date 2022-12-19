# -*- coding: utf-8 -*-

import scrapy
import datetime
from travel.items import Notes

class NotesFileSpider(scrapy.Spider):
    name = "notes_file"

    start_urls = [
        "https://you.ctrip.com/travels/",
    ]

    def parse(self, response):
        notes = response.css("div.city")

        item = Notes()
        time = datetime.date.today()

        for note in notes:
            yield{
                # 'text': quote.css("span.text::text").get(),
                # 'author': quote.css("small.author::text").get(),
                # 'tags': quote.css("div.tags a.tag::text").getall()

                'name': note.css("div.city-sub a.city-name::text").get(),
                'time': str(time),
                'view': note.css("div.city-sub p.opts i.numview::text").get(),
                'like': note.css("div.city-sub p.opts i.want::text").get(),
                'reply': note.css("div.city-sub p.opts i.numreply::text").get(),
                'note_url': "https://you.ctrip.com" + note.css("div.city-sub a.cpt::attr(href)").get()
            }