#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('旅游数据统计之city').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

dbUrl = "jdbc:mysql://192.168.*.*:*/travel?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT%2B8"
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
who_dic = {city: {} for city in city_keys}
day_dic = {city: {} for city in city_keys}
month_dic = {city: {} for city in city_keys}
ent_dic = {city: {} for city in city_keys}
money_dic = {city: 0 for city in city_keys}
money_num_dic = {city: 0 for city in city_keys}

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
                if city == "三亚":
                    city_key = 'Sanya'
                elif city == "香港":
                    city_key = 'HongKong'
                elif city == "成都":
                    city_key = 'Chengdu'
                elif city == "丽江":
                    city_key = 'Lijiang'
                elif city == "厦门":
                    city_key = 'Xiamen'
                elif city == "杭州":
                    city_key = 'Hangzhou'
                else:
                    continue

                if who is not None:
                    if who in who_dic[city_key]:
                        who_dic[city_key][who] += 1
                    else:
                        who_dic[city_key][who] = 1
                if days is not None:
                    if days in day_dic[city_key]:
                        who_dic[city_key][days] += 1
                    else:
                        who_dic[city_key][days] = 1
                if month is not None:
                    if month != "":
                        if month in month_dic[city_key]:
                            month_dic[city_key][month] += 1
                        else:
                            month_dic[city_key][month] = 1
                if money is not None:
                    if "元" in money:
                        money_dic[city_key] += int(money.split("元")[0])
                        money_num_dic[city_key] += 1
                if ent is not None:
                    ent_list = ent.split("，")
                    for element in ent_list:
                        if element in ent_dic:
                            ent_dic[city_key][element] += 1
                        else:
                            ent_dic[city_key][element] = 1

max_who = [max(who_dic[city_key], key=who_dic[city_key].get) for city_key in city_keys]
max_month = [max(month_dic[city_key], key=month_dic[city_key].get) for city_key in city_keys]
max_days = [max(days_dic[city_key], key=days_dic[city_key].get) for city_key in city_keys]
max_ent = [max(ent_dic[city_key], key=ent_dic[city_key].get) for city_key in city_keys]
max_money = [int(money_dic[city_key] / money_num_dic[city_key].get) for city_key in city_keys]
   
city_names = ['三亚', '香港', '成都', '丽江', '厦门', '杭州']
analysis_list = [[(city_names[i], max_who[i], max_days[i], max_month[i], max_money[i], max_ent[i])] for i in range(len(city_names))]

whoSchema = StructType(
    [
        StructField('city', StringType(), True),
        StructField('who', StringType(), True),
        StructField('days', StringType(), True),
        StructField('month', StringType(), True),
        StructField('money', IntegerType(), True),
        StructField('ent', StringType(), True)
    ]
)

RDDlist = [ss.sparkContext.parallelize(analysis) for analysis in analysis_list]

RowsRDDlist = [RDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1],
        noteRow[2],
        noteRow[3],
        noteRow[4],
        noteRow[5])) for RDD in RDDlist]

analysisDFlist = [ss.createDataFrame(rowsRDD, whoSchema) for rowsRDD in RowsRDDlist]

for i in range(len(city_keys)):
    analysisDFlist[i].write.format("jdbc").option("url", dbUrl).option("dbtable", "recommand_city").option("user", "root").option("password", "yourpassword").mode('append').save()
