#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('热门旅游城市who').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

dbUrl = "jdbc:mysql://192.168.*.*:*/travel?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT%2B8"
dbProperties = {
    "user": "root",
    "password": "yourpassword",
    "driver": "com.mysql.jdbc.Driver"
}

who_keys = ['with_friend', 'with_child', 'with_couple', 'with_alone', 'with_lover', 'with_parent']

notesDF_list = [ss.read.jdbc(dbUrl, who_key, properties=dbProperties) for who_key in who_keys]

cityCount = [{} for i in range(len(who_keys))]

for i in range(len(who_keys)):
    for note in notesDF_list[i].collect():
        city = note['city']
        if city in cityCount[i]:
            cityCount[i][city] += 1
        else:
            cityCount[i][city] = 1

who_names = ['和朋友', '亲子', '夫妻', '一个人', '情侣', '和父母']

analysis_list = [[(who_names[i], city, cityCount[i][city]) for city in cityCount[i]] for i in range(len(who_names))]

countSchema = StructType(
    [
        StructField('who', StringType(), True),
        StructField('city', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

RDDlist = [ss.sparkContext.parallelize(analysis) for analysis in analysis_list]
RowsRDDlist = [noteRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1],
        noteRow[2]
    )
) for noteRDD in RDDlist]

noteAnalysisDF_list = [ss.createDataFrame(noteRowsRDD, countSchema)for noteRowsRDD in RowsRDDlist]
dbtables = ["friend_city_count", "child_city_count", "couple_city_count", "alone_city_count", "lover_city_count", "parent_city_count"]

for i in range(len(dbtables)):
    noteAnalysisDF_list[i].write.format("jdbc").option("url", dbUrl).option("dbtable", dbtables[i]).option("user", "root").option("password", "yourpassword").mode('append').save()
