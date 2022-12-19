#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*') \
    .appName('热门游记相关城市统计') \
    .config('spark.python.worker.memory', '200g') \
    .config('spark.python.driver.memory', '100g') \
    .config('spark.python.executor.memory', '80g') \
    .getOrCreate()

dbUrl = "jdbc:mysql://192.168.*.*:*/travel?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT%2B8"
dbProperties = {
    "user": "root",
    "password": "yourpassword"",
    "driver": "com.mysql.jdbc.Driver"
}

today = datetime.date.today()

notesDF = ss.read.jdbc(
    dbUrl,
    "notes",
    predicates=["time='" + str(today) + "'"],
    properties=dbProperties
)

noteCount = {}
viewCount = {}
likeCount = {}
replyCount = {}

for note in notesDF.collect():
    city = note['city']
    view = note['view']
    like = note['like']
    reply = note['reply']

    if city in noteCount:
        noteCount[city] += 1
        viewCount[city] += int(view)
        likeCount[city] += int(like)
        replyCount[city] += int(reply)
    else:
        noteCount[city] = 1
        viewCount[city] = int(view)
        likeCount[city] = int(like)
        replyCount[city] = int(reply)

noteAnalysis = [(city, noteCount[city], viewCount[city], likeCount[city], replyCount[city]) for city in noteCount]

noteAnalysisSort = sorted(noteAnalysis, key=lambda noteItem: noteItem[2], reverse=True)

countSchema = StructType(
    [
        StructField('date', StringType(), True),
        StructField('city', StringType(), True),
        StructField('note', IntegerType(), True),
        StructField('view', IntegerType(), True),
        StructField('like', IntegerType(), True),
        StructField('reply', IntegerType(), True)
    ]
)

noteRDD = ss.sparkContext.parallelize(noteAnalysisSort)
noteRowsRDD = noteRDD.map(
    lambda noteRow: Row(
        str(today),
        noteRow[0],
        noteRow[1],
        noteRow[2],
        noteRow[3],
        noteRow[4]
    )
)
noteAnalysisDF = ss.createDataFrame(noteRowsRDD, countSchema)

noteAnalysisDF.write.format("jdbc") \
    .option("url", dbUrl) \
    .option("dbtable", "notes_count") \
    .option("user", "root").option("password", "yourpassword") \
    .mode('append').save()
