# -*- coding: utf-8 -*-

from travel.settings import MYSQL_URI, MYSQL_DATABASE
import pymysql.cursors

class MysqlPipeline(object):
    def __init__(self):
        self.mysql_url = MYSQL_URI
        self.mysql_db = MYSQL_DATABASE
    
    def open_spider(self, spider):
        self.mysql_conn = pymysql.connect(
            host = self.mysql_url,
            user = "root",
            db = self.mysql_db,
            password = "yourpassword",
            charset = "utf8mb4",
            cursorclass = pymysql.cursors.DictCursor
        )

    def process_item(self, item, spider):

        try:
            with self.mysql_conn.cursor() as cursor:

                #sql_write = "INSERT INTO `notes` (`city`, `time`, `view`, `like`, `reply`, `note_url`) VALUES (%s, %s, %s, %s, %s, %s)"
                #cursor.execute(sql_write, (item.get("city", ""), item.get("time", ""), item.get("view", ""), item.get("like", ""), item.get("reply", ""), item.get("note_url", "")))

                sql_write = "INSERT INTO `notes_content_new` (`date`, `city`, `content`, `days`, `when`, `money`, `with_whom`, `entertainment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_write, (item.get("date", ""), item.get("city", ""), item.get("content", ""), item.get("days", ""), item.get("when", ""), item.get("money", ""), item.get("with_whom", ""), item.get("entertainment", "")))

            self.mysql_conn.commit()

        except Exception as e:
            print(e)

        return item

    def close_spidr(self, spider):
        self.mysql_conn.close()

