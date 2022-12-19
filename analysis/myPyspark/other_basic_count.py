#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

ss = SparkSession.builder.master('spark://192.168.*.*:*').appName('旅游数据统计').config('spark.python.worker.memory', '200g').config('spark.python.driver.memory', '100g').config('spark.python.executor.memory', '80g').getOrCreate()

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

monthCount = {}
daysCount = {"1-2天": 0, "3-5天": 0, "6-8天": 0, "9-14天": 0, "15天以上": 0}
moneyCount = {}
numCount = {}
whoCount = {}
entCount = {}

for note in notesDF.collect():
    if note['date'] is not None:
        if note['date'] != "NO_TIME":
            if "-" in note['date']:
                year = note['date'].split("-")[0]
            elif "." in note['date']:
                year = note['date'].split(".")[0]
            else:
                year = "" + 1900
            month = note['when']
            days = note['days']
            money = note['money']
            who = note['with_whom']
            ent = note['entertainment']
            if int(year) >= 2014:
                if month is not None:
                    if month in monthCount:
                        monthCount[month] += 1
                    else:
                        monthCount[month] = 1
                if days is not None:
                    if "天" in days:
                        days_num = int(days.split("天")[0])
                        if days_num < 3:
                            daysCount["1-2天"] += 1
                        elif days_num < 6:
                            daysCount["3-5天"] += 1
                        elif days_num < 9:
                            daysCount["6-8天"] += 1
                        elif days_num < 15:
                            daysCount["9-14天"] += 1
                        else:
                            daysCount["15天以上"] += 1
                if money is not None:
                    if "元" in money:
                        new_money = int(money.split("元")[0])
                        if year in moneyCount:
                            numCount[year] += 1
                            moneyCount[year] += new_money
                        else:
                            numCount[year] = 1
                            moneyCount[year] = new_money
                if who is not None:
                    if who in whoCount:
                        whoCount[who] += 1
                    else:
                        whoCount[who] = 1
                if ent is not None:
                    ent_list = ent.split("，")
                    for element in ent_list:
                        if element in entCount:
                            entCount[element] += 1
                        else:
                            entCount[element] = 1

monthAnalysis = [(month, monthCount[month]) for month in monthCount]
daysAnalysis = [(days, daysCount[days]) for day in daysCount]
moneyAnalysis = [(year, moneyCount[year], numCount[year], int(moneyCount[year] / numCount[year])) for year in moneyCount]
whoAnalysis = [(who, whoCount[who]) for who in whoCount]
entAnalysis = [(ent, entCount[ent]) for ent in entCount]

monthAnalysisSort = sorted(monthAnalysis, key=lambda noteItem: noteItem[1], reverse=True)
daysAnalysisSort = sorted(daysAnalysis, key=lambda noteItem: noteItem[1], reverse=True)
moneyAnalysisSort = sorted(moneyAnalysis, key=lambda noteItem: noteItem[0])
whoAnalysisSort = sorted(whoAnalysis, key=lambda noteItem: noteItem[1], reverse=True)
entAnalysisSort = sorted(entAnalysis, key=lambda noteItem: noteItem[1], reverse=True)

monthSchema = StructType(
    [
        StructField('month', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

daysSchema = StructType(
    [
        StructField('days', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

moneySchema = StructType(
    [
        StructField('year', StringType(), True),
        StructField('money', IntegerType(), True),
        StructField('count', IntegerType(), True),
        StructField('ave', IntegerType(), True)
    ]
)

whoSchema = StructType(
    [
        StructField('who', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

entSchema = StructType(
    [
        StructField('ent', StringType(), True),
        StructField('count', IntegerType(), True)
    ]
)

monthRDD = ss.sparkContext.parallelize(monthAnalysisSort)
daysRDD = ss.sparkContext.parallelize(daysAnalysisSort)
moneyRDD = ss.sparkContext.parallelize(moneyAnalysisSort)
whoRDD = ss.sparkContext.parallelize(whoAnalysisSort)
entRDD = ss.sparkContext.parallelize(entAnalysisSort)

monthRowsRDD = monthRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1]
    )
)
daysRowsRDD = daysRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1]
    )
)
moneyRowsRDD = moneyRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1],
        noteRow[2],
        noteRow[3]
    )
)
whoRowsRDD = whoRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1]
    )
)
entRowsRDD = entRDD.map(
    lambda noteRow: Row(
        noteRow[0],
        noteRow[1]
    )
)

monthAnalysisDF = ss.createDataFrame(monthRowsRDD, monthSchema)
daysAnalysisDF = ss.createDataFrame(daysRowsRDD, daysSchema)
moneyAnalysisDF = ss.createDataFrame(moneyRowsRDD, moneySchema)
whoAnalysisDF = ss.createDataFrame(whoRowsRDD, whoSchema)
entAnalysisDF = ss.createDataFrame(entRowsRDD, entSchema)

monthAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "month_count").option("user", "root").option("password", "yourpassword").mode('append').save()
daysAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "days_count").option("user", "root").option("password", "yourpassword").mode('append').save()
moneyAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "money_count").option("user", "root").option("password", "yourpassword").mode('append').save()
whoAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "who_count").option("user", "root").option("password", "yourpassword").mode('append').save()
entAnalysisDF.write.format("jdbc").option("url", dbUrl).option("dbtable", "ent_count").option("user", "root").option("password", "yourpassword").mode('append').save()
