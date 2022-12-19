# -*- coding: utf-8 -*-

import scrapy
import datetime
from travel.items import Notes


class NotesSQLSpider(scrapy.Spider):
    name = "notes_mysql"

    start_urls = [
        "https://you.ctrip.com/travels/",
    ]

    def parse(self, response):
        notes = response.css("div.city")

        item = Notes()
        time = datetime.date.today()

        for note in notes:
            name = note.css("div.city-sub a.city-name::text").get()
            item['city'] = name
            item['time'] = str(time)
            view = note.css("div.city-sub p.opts i.numview::text").get()
            item['view'] = view
            want = note.css("div.city-sub p.opts i.want::text").get()
            item['like'] = want
            reply = note.css("div.city-sub p.opts i.numreply::text").get()
            item['reply'] = reply
            href = note.css("div.city-sub a.cpt::attr(href)").get()
            note_url = "https://you.ctrip.com" + href
            item['note_url'] = note_url
            yield item