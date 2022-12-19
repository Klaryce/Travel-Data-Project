#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:****').appName('旅游数据之accommodation统计').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

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

hotel = ["酒店", "宾馆", "旅馆"]
homestay = ["民宿"]

accomCount = {}
accomCount["酒店"] = 0
accomCount["民宿"] = 0

friendAnalysis = []

for note in notesDF.collect():
    if note['date'] is not None:
        if note['date'] != "NO_TIME":
            if "-" in note['date']:
                year = note['date'].split("-")[0]
            elif "." in note['date']:
                year = note['date'].split(".")[0]
            else:
                year = "" + 1900
            content = note['content']
            if int(year) >= 2014:
                if content is not None:
                    for element in hotel:
                        if element in content:
                            accomCount["酒店"] += 1
                            break
                    for element in homestay:
                        if element in content:
                            accomCount["民宿"] += 1
                            break

for traff in accomCount:
    friendAnalysis.append((traff, accomCount[traff]))

friendSchema = StructType(
    [
        StructField('accom', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)


friendRDD = ss.sparkContext.parallelize(friendAnalysis)

friendRowsRDD = friendRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1]
    )
)

friendAnalysisDF = ss.createDataFrame(friendRowsRDD, friendSchema)

friendAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "accom_count").option("user", "root").option("password", "yourpassword").mode('append').save()

