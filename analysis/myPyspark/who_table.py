#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('旅游数据之与谁出行统计').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

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

who_names = ['和朋友', '亲子', '夫妻', '一个人', '情侣', '和父母']

analysis_dic = {who: [] for who in who_names}

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
                if who is not None:
                    if who in who_names:
                        analysis_dic[who].append((who, city, days, month, money, ent))

schema_list = [StructType(
    [
        StructField('who', StringType(), True),
        StructField('city', StringType(), True),
        StructField('days', StringType(), True),
        StructField('when', StringType(), True),
        StructField('money', StringType(), True),
        StructField('ent', StringType(), True)
    ]
) for i in range(len(who_names))]

RDDlist = [ss.sparkContext.parallelize(analysis_dic[who_name]) for who_name in analysis_dic]
RowsRDDlist = [RDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1],
        noteRow[2],
        noteRow[3],
        noteRow[4],
        noteRow[5]
    )
) for RDD in RDDlist]

analysisDF_list = [ss.createDataFrame(RowsRDDlist[i], schema_list[i]) for i in range(len(who_names))]

dbtables = ['with_friend', "with_child", "with_couple", "with_alone", "with_lover", "with_parent"]

for i in range(len(dbtables)):
    analysisDF_list[i].write.format("jdbc").option("url", dbUrl).option("dbtable", dbtables[i]).option("user", "root").option("password", "yourpassword").mode('append').save()
