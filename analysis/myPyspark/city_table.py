#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*.:*').appName('旅游数据之出行城市统计').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

dbUrl = "jdbc:mysql://192.168.*.*.:*/travel?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT%2B8"
dbProperties = {
    "user": "root",
    "password": "yourpassword",
    "driver": "com.mysql.jdbc.Driver"
}


notesDF = ss.read.jdbc(
    dbUrl,
    "notes_content_new",
    properties=dbProperties
)

city_keys = ['Sanya', 'HongKong', 'Chengdu', 'Lijiang', 'Xiamen', 'Hangzhou']

city_analysis = {city: [] for city in city_keys}

for note in notesDF.collect():
    if note['date'] is not None:
        if note['date'] != "NO_TIME":
            if "-" in note['date']:
                year = note['date'].split("-")[0]
            elif "." in note['date']:
                year = note['date'].split(".")[0]
            else:
                year = "" + 1900
            city = note['city']
            month = note['when']
            days = note['days']
            money = note['money']
            who = note['with_whom']
            ent = note['entertainment']
            if int(year) >= 2014:
                if city is not None:
                    if city == "三亚":
                        city_analysis['Sanya'].append((city, days, month, money, who, ent))
                    elif city == "香港":
                        city_analysis['HongKong'].append((city, days, month, money, who, ent))
                    elif city == "成都":
                        city_analysis['Chengdu'].append((city, days, month, money, who, ent))
                    elif city == "丽江":
                        city_analysis['Lijiang'].append((city, days, month, money, who, ent))
                    elif city == "厦门":
                        city_analysis['Xiamen'].append((city, days, month, money, who, ent))
                    elif city == "杭州":
                        city_analysis['Hangzhou'].append((city, days, month, money, who, ent))

field_names = ['city', 'days', 'when', 'money', 'who', 'ent']
schema_list = [StructType([StructField(field_name, StringType(), True) for field in field_names]) for i in range(len(city_keys))]

RDDlist = [ss.sparkContext.parallelize(city_analysis[city]) for city in city_analysis]
RowsRDDlist = [RDD.map(lambda noteRow: Row(noteRow[0], noteRow[1], noteRow[2], noteRow[3], noteRow[4], noteRow[5])) for RDD in RDDlist]

analysisDFlist = [ss.createDataFrame(RowsRDDlist[i], schema_list[i]) for i in range(len(city_keys))]

dbtables = ["city_sanya", "city_hongkong", "city_chengdu", "city_lijiang", "city_xiamen", "city_hangzhou"]

for i in range(len(cities)):
    analysisDFlist[i].write.format("jdbc").option("url", dbUrl).option("dbtable", dbtables[i]).option("user", "root").option("password", "yourpassword").mode('append').save()

