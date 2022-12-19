# -*- coding: utf-8 -*-

import scrapy
import datetime
from travel.items import NotesContent
import csv

this_url = ""
has = 0

class ContentFileSpider(scrapy.Spider):
    name = "content2_mysql"

    def start_requests(self):
        global this_url
        with open('notes2.csv', 'r', encoding="utf-8", newline='\n') as fin_0:
            cr_0 = csv.reader(fin_0)
            all_data = [line for line in cr_0]

        urls = []

        for data in all_data:
            if data[2] != "note_url":
                urls.append(data[2])

        for url in urls:
            this_url = url
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        global this_url, has
        content = response.css("div.ctd_content p::text").getall()
        has = 0
        if response.css("body > div.bgf2f2f2 > div.content.cf > div.ctd_main > div.ctd_main_body > div.ctd_content > h3::text").get() is not None:
            date_ = response.css("body > div.bgf2f2f2 > div.content.cf > div.ctd_main > div.ctd_main_body > div.ctd_content > h3::text").get().split()[1]
            has = 1
        elif response.css("div.ctd_head_con.cf div.time::text").get() is not None:
            date_ = response.css("div.ctd_head_con.cf div.time::text").get()
            has = 1
        elif response.css("div.ctd_head_left p::text").getall() is not None:
            if len(response.css("div.ctd_head_left p::text").getall()) > 1:
                if len(response.css("div.ctd_head_left p::text").getall()[1].split("：")) > 1:
                    date_ = response.css("div.ctd_head_left p::text").getall()[1].split("：")[1].strip()
                    has = 1
        if has == 0 and response.css("div.ctd_head_left h2::attr(data-publishdate)").get().split()[0] is not None:
            date_ = response.css("div.ctd_head_left h2::attr(data-publishdate)").get().split()[0]
            has = 1
        if has == 0:
            date_ = "NO_TIME"
        
        item = NotesContent()

        item['content'] = ""
        item['date'] = str(date_)

        if response.css("ul.ctd_des_list.cf li h3::text").get() is not None:
            item['city'] = response.css("ul.ctd_des_list.cf li h3::text").get()
        elif response.css("ul.ctd_ttd li h4::text").get() is not None:
            item['city'] = response.css("ul.ctd_ttd li h4::text").get()
        else:
            item['city'] = ""

        item['days'] = ""
        item['when'] = ""
        item['money'] = ""
        item['with_whom'] = ""
        item['entertainment'] = ""

        if response.css("div.ctd_content_controls.cf div.bottom span::text").get() is not None:
            info = response.css("div.ctd_content_controls.cf div.bottom span::text").getall()
            for i in info:
                if i.split("：")[0] == "天数":
                    item['days'] = i.split("：")[1]
                if i.split("：")[0] == "时间":
                    item['when'] = i.split("：")[1]
                if i.split("：")[0] == "人均":
                    item['money'] = i.split("：")[1]
                if i.split("：")[0] == "和谁":
                    item['with_whom'] = i.split("：")[1]
                if i.split("：")[0] == "玩法":
                    item['entertainment'] = i.split("：")[1]
        elif response.css("div.ctd_content_controls.cf span::text").get() is not None:
            info = response.css("div.ctd_content_controls.cf span::text").getall()
            for i in info:
                if i.split("：")[0] == "天数":
                    item['days'] = i.split("：")[1]
                if i.split("：")[0] == "时间":
                    item['when'] = i.split("：")[1]
                if i.split("：")[0] == "人均":
                    item['money'] = i.split("：")[1]
                if i.split("：")[0] == "和谁":
                    item['with_whom'] = i.split("：")[1]
                if i.split("：")[0] == "玩法":
                    item['entertainment'] = i.split("：")[1]
        elif response.css("div.w_journey dl dt span::text").get() is not None:
            info = response.css("div.w_journey dl dt span::text").getall()
            for i in info:
                if i.split("：")[0] == "天数":
                    item['days'] = i.split("：")[1]
                if i.split("：")[0] == "时间":
                    item['when'] = i.split("：")[1]
                if i.split("：")[0] == "人均":
                    item['money'] = i.split("：")[1]
                if i.split("：")[0] == "和谁":
                    item['with_whom'] = i.split("：")[1]
                if i.split("：")[0] == "玩法":
                    item['entertainment'] = i.split("：")[1]
        
        for line in content:
            item['content'] += line

        yield item