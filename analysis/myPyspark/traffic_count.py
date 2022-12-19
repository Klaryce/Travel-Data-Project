#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('旅游数据之交通统计').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

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

train = ["火车", "高铁", "动车"]
plane = ["飞机", "机场", "机票"]
drive = ["自驾", "开车"]

trafficCount = {"火车": 0, "飞机": 0, "自驾": 0}

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
                    for element in train:
                        if element in content:
                            trafficCount["火车"] += 1
                            break
                    for element in plane:
                        if element in content:
                            trafficCount["飞机"] += 1
                            break
                    for element in drive:
                        if element in content:
                            trafficCount["自驾"] += 1
                            break

friendAnalysis = [(traff, trafficCount[traff]) for traff in trafficCount]

friendSchema = StructType(
    [
        StructField('traffic', StringType(), True),
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

friendAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "traffic_count").option("user", "root").option("password", "yourpassword").mode('append').save()

