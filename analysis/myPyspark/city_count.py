#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:****') \
    .appName('热门旅游城市') \
    .config('spark.python.worker.memory', '200g') \
    .config('spark.python.driver.memory', '100g') \
    .config('spark.python.executor.memory', '80g') \
    .getOrCreate()

dbUrl = "jdbc:mysql://192.168.*.*:****/travel?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT%2B8"
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

cityCount = {}

for note in notesDF.collect():
    if note['date'] is not None:
        if note['date'] != "NO_TIME":
            if "-" in note['date']:
                year = note['date'].split("-")[0]
            elif "." in note['date']:
                year = note['date'].split(".")[0]
            else:
                year = 1900

            city = note['city']

            if int(year) >= 2014:
                if city in cityCount:
                    cityCount[city] += 1
                else:
                    cityCount[city] = 1

noteAnalysis = []
for city in cityCount:
    noteAnalysis.append((city, cityCount[city]))

noteAnalysisSort = sorted(noteAnalysis, key=lambda noteItem: noteItem[1], reverse=True)

countSchema = StructType(
    [
        StructField('city', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

noteRDD = ss.sparkContext.parallelize(noteAnalysisSort)
noteRowsRDD = noteRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1]
    )
)
noteAnalysisDF = ss.createDataFrame(noteRowsRDD, countSchema)

noteAnalysisDF.write.format("jdbc") \
    .option("url", dbUrl) \
    .option("dbtable", "city_count") \
    .option("user", "root").option("password", "yourpassword") \
    .mode('append').save()
