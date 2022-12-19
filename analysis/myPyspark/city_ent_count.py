#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('热门旅游玩法city').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

dbUrl = "jdbc:mysql://192.168.*.*:*/travel?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=GMT%2B8"
dbProperties = {
    "user": "root",
    "password": "yourpassword",
    "driver": "com.mysql.jdbc.Driver"
}

cities = ["city_sanya", "city_hongkong", "city_chengdu", "city_lijiang", "city_xiamen", "city_hangzhou"]
city_names = ["三亚(Sanya)", "香港(HK)", "成都(Chengdu)", "丽江(Lijiang)", "厦门(Xiamen)", "杭州(Hangzhou)"]

notesDF_list = [ss.read.jdbc(dbUrl, city, properties=dbProperties) for city in cities]

for i in range(len(cities)):
    cityCount_list.append({})
    for note in notesDF_list[i].collect():
        if note['ent'] is not None:
            ent_list = note['ent'].split("，")
            for element in ent_list:
                if element in cityCount_list[i]:
                    cityCount_list[i][element] += 1
                else:
                    cityCount_list[i][element] = 1

noteAnalysis_list[[(city_names[i], city, cityCount_list[i][city]) for city in cityCount_list[i]] for i in range(len(cities))]


# print(sorted(noteAnalysis, key=lambda noteItem: noteItem[1], reverse=True))

countSchema = StructType(
    [
        StructField('city', StringType(), True),
        StructField('ent', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

noteRDD_list = [ss.sparkContext.parallelize(noteAnalysis_list[i] for i in range(len(cities)))]

noteRowsRDD_list = [noteRDD.map(lambda noteRow: Row(noteRow[0], noteRow[1], noteRow[2])) for noteRDD in noteRDD_list]

noteAnalysisDF_list = [ss.createDataFrame(noteRowsRDD, countSchema) for noteRowsRDD in noteRowsRDD_list]

dbtables = ["ent_count_sanya", "ent_count_hongkong", "ent_count_chengdu", "ent_count_lijiang", "ent_count_xiamen", "ent_count_hangzhou"]
for i in range(len(cities)):
    noteAnalysisDF_list[i].write.format("jdbc").option("url", dbUrl).option("dbtable", dbtables[i]).option("user", "root").option("password", "yourpassword").mode('append').save()
