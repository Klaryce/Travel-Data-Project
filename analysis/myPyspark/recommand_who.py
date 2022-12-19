#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('旅游数据统计之friend').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

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

who_keys = ['friend', 'child', 'couple', 'alone', 'lover', 'parent']
city_dic = {who: {} for who in who_keys}
days_dic = {who: {} for who in who_keys}
month_dic = {who: {} for who in who_keys}
ent_dic = {who: {} for who in who_keys}
money_dic = {who: 0 for who in who_keys}
money_num_dic = {who: 0 for who in who_keys}

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
                if who == "和朋友":
                    who_key = 'friend'
                elif who == "亲子":
                    who_key = 'child'
                elif who == "夫妻":
                    who_key = 'couple'
                elif who == "一个人":
                    who_key = 'along'
                elif who == "情侣":
                    who_key = 'lover'
                elif who == "和父母":
                    who_key = 'parent'
                else:
                    continue

                if city is not None:
                    if city in city_dic:
                        city_dic[who_key][city] += 1
                    else:
                        city_dic[who_key][city] = 1
                if days is not None:
                    if days in days_dic:
                        days_dic[who_key][days] += 1
                    else:
                        days_dic[who_key][days] = 1
                if month is not None:
                    if month in month_dic:
                        month_dic[who_key][month] += 1
                    else:
                        month_dic[who_key][month] = 1
                if money is not None:
                    if "元" in money:
                        money_dic[who_key] += int(money.split("元")[0])
                        money_num_dic[who_key] += 1
                if ent is not None:
                    ent_list = ent.split("，")
                    for element in ent_list:
                        if element in ent_dic:
                            ent_dic[who_key][element] += 1
                        else:
                            ent_dic[who_key][element] = 1

max_city = [max(city_dic[who_key], key=city_dic[who_key].get) for who_key in who_keys]
max_month = [max(month_dic[who_key], key=month_dic[who_key].get) for who_key in who_keys]
max_days = [max(days_dic[who_key], key=days_dic[who_key].get) for who_key in who_keys]
max_ent = [max(ent_dic[who_key], key=ent_dic[who_key].get) for who_key in who_keys]
max_money = [int(money_dic[who_key] / money_num_dic[who_key].get) for who_key in who_keys]

who_names = ['和朋友', '亲子', '夫妻', '一个人', '情侣', '和父母']
analysis_list = [[(who_names[i], max_city[i], max_days[i], max_month[i], max_money[i], max_ent[i])] for i in range(len(who_names))]

whoSchema = StructType(
    [
        StructField('who', StringType(), True),
        StructField('city', StringType(), True),
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
    analysisDFlist[i].write.format("jdbc").option("url", dbUrl).option("dbtable", "recommand_who").option("user", "root").option("password", "yourpassword").mode('append').save()