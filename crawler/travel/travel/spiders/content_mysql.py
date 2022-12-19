# -*- coding: utf-8 -*-

import scrapy
import datetime
from travel.items import NotesContent
import csv


class ContentFileSpider(scrapy.Spider):
    name = "content_mysql"

    def start_requests(self):
        with open('notes.csv', 'r', encoding="utf-8", newline='\n') as fin_0:
            cr_0 = csv.reader(fin_0)
            all_data = [line for line in cr_0]

        urls = []

        for data in all_data:
            if data[5] != "note_url":
                urls.append(data[5])

        #urls = ["https://you.ctrip.com/travels/changshu101/3950184.html"] # check single url

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        content = response.css("div.ctd_content p::text").getall()
        if response.css("body > div.bgf2f2f2 > div.content.cf > div.ctd_main > div.ctd_main_body > div.ctd_content > h3::text").get() is not None:
            date_ = response.css("body > div.bgf2f2f2 > div.content.cf > div.ctd_main > div.ctd_main_body > div.ctd_content > h3::text").get().split()[1]
            #date_ = datetime.datetime.strptime(date_, '%Y-%m-%d')
        elif response.css("div.ctd_head_con.cf div.time::text").get() is not None:
            date_ = response.css("div.ctd_head_con.cf div.time::text").get()
        else:
            date_ = "error"

        item = NotesContent()
        #date = datetime.date.today()

        item['content'] = ""
        item['date'] = str(date_)
        item['days'] = ""
        item['when'] = ""
        item['money'] = ""
        item['who'] = ""
        if response.css("div.ctd_content_controls.cf div.bottom span::text").get() is not None:
            info = response.css("div.ctd_content_controls.cf div.bottom span::text").getall()
            for i in info:
                if i.split("：")[0] == "天数":
                    item['days'] = i.split("：")[1]
                if i.split("：")[0] == "时间":
                    item['time'] = i.split("：")[1]
                if i.split("：")[0] == "人均":
                    item['money'] = i.split("：")[1]
                if i.split("：")[0] == "和谁":
                    item['with_who'] = i.split("：")[1]
        
        for line in content:
            item['content'] += line

        yield item