# -*- coding:utf-8 -*-
import json
from flask import Blueprint, jsonify, request
from config import db
from dbmodel.simple_count import CityCount, DaysCount, MoneyCount, MonthCount, TrafficCount, EntCount, WhoCount, AccomCount, TourCount
from dbmodel.city_recommend import Sanya, Chengdu, Lijiang, Xiamen, Hangzhou, Hongkong
from dbmodel.who_recommend import Friend, Child, Couple, Alone, Lover, Parent
from .form import *

"""
本视图专门用于处理ajax数据
"""
data = Blueprint('data', __name__)


@data.route('/getMap', methods=['GET'])
def get_map():
    data = db.session.query(CityCount).order_by(CityCount.count.desc()).all()
    view_data = {}
    view_data["series"] = []

    def build_view_data(item):
        dic = {}
        dic["value"] = item.count
        dic["name"] = item.city
        view_data["series"].append([dic])

    for i in range(30):
        build_view_data(data[i])

    return json.dumps(view_data, ensure_ascii=False)


@data.route('/getDaysCount', methods=['GET'])
def get_days_count():
    view_data = {}
    view_data["series"] = []

    data = []
    days_list = ["1-2天", "3-5天", "6-8天", "9-14天", "15天以上"]
    for days_str in days_list:
        data1 = db.session.query(DaysCount).filter_by(days=days_str).first()
        data.append(data1)


    def build_view_data(item):
        dic = {}
        dic["value"] = item.count
        dic["name"] = item.days
        view_data["series"].append(dic)

    [build_view_data(item) for item in data]

    return json.dumps(view_data, ensure_ascii=False)

@data.route('/getAccomCount', methods=['GET'])
def get_accom_count():
    view_data = {}
    view_data["series"] = []

    data = db.session.query(AccomCount).all()

    def build_view_data(item):
        dic = {}
        dic["value"] = item.count
        dic["name"] = item.accom
        view_data["series"].append(dic)

    [build_view_data(item) for item in data]

    return json.dumps(view_data, ensure_ascii=False)

@data.route('/getTourCount', methods=['GET'])
def get_tour_count():
    view_data = {}
    view_data["series"] = []

    data = db.session.query(TourCount).all()

    def build_view_data(item):
        dic = {}
        dic["value"] = item.count
        dic["name"] = item.tour
        view_data["series"].append(dic)

    [build_view_data(item) for item in data]

    return json.dumps(view_data, ensure_ascii=False)

@data.route('/getMonthCount', methods=['GET'])
def get_month_count():
    data = db.session.query(MonthCount).all()
    view_data = {}
    view_data["xAxis"] = ["2 月", "3 月", "4 月", "5 月", "6 月", "7 月", "8 月", "9 月", "10 月", "11 月", "12 月", "1 月"]
    view_data["series1"] = []
    all_area = ["2 月", "3 月", "4 月", "5 月", "6 月", "7 月", "8 月", "9 月", "10 月", "11 月", "12 月", "1 月"]
    view_data["count"] = []

    def build_view_data(item):
        tmp_dic = {}
        tmp_dic["value"] = item.count
        tmp_dic["name"] = item.month
        view_data["series1"].append(tmp_dic)
        view_data["count"].append(item.count)

    [build_view_data(item) for i in all_area for item in data if item.month == i]

    print(view_data)

    return json.dumps(view_data, ensure_ascii=False)


@data.route('/getMoneyTrend', methods=['GET'])
def get_money_trend():
    data = db.session.query(MoneyCount).order_by(MoneyCount.year.asc()).all()
    view_data = {}
    view_data["xAxis"] = []
    view_data["series1"] = []

    def build_view_data(item):
        view_data["xAxis"].append(item.year)
        view_data["series1"].append(item.ave)

    [build_view_data(item) for item in data]

    return json.dumps(view_data, ensure_ascii=False)


@data.route('/getEntCount', methods=['GET'])
def get_ent_count():
    data = db.session.query(EntCount).order_by(EntCount.count.desc()).all()
    view_data = {}
    view_data["series1"] = []

    def build_view_data(item):
        view_data["series1"].append(item.ent)

    for i in range(15):
        build_view_data(data[i])

    return json.dumps(view_data, ensure_ascii=False)


@data.route('/getWhoCount', methods=['GET'])
def get_who_count():
    data = db.session.query(WhoCount).all()
    view_data = {}
    view_data["series1"] = []

    def build_view_data(item):
        tmp_dic = {}
        tmp_dic["name"] = item.who
        tmp_dic["value"] = item.count
        view_data["series1"].append(tmp_dic)

    [build_view_data(item) for item in data]

    return json.dumps(view_data, ensure_ascii=False)

@data.route('/getTrafficCount', methods=['GET'])
def get_traffic_count():

    data = db.session.query(TrafficCount).order_by(TrafficCount.count.desc()).all()

    view_data = {}
    view_data["series"] = []

    def build_view_data(item):
        view_data["series"].append({"value": item.count, "name": item.traffic})

    [build_view_data(item) for item in data]

    return json.dumps(view_data, ensure_ascii=False)

@data.route('/entCountCity/<city>', methods=['GET'])
def ent_count_city(city):
    view_data = {}
    if city == "三亚":
        data = db.session.query(Sanya).order_by(Sanya.count.desc()).all()
    elif city == "成都":
        data = db.session.query(Chengdu).order_by(Chengdu.count.desc()).all()
    elif city == "丽江":
        data = db.session.query(Lijiang).order_by(Lijiang.count.desc()).all()
    elif city == "厦门":
        data = db.session.query(Xiamen).order_by(Xiamen.count.desc()).all()
    elif city == "杭州":
        data = db.session.query(Hangzhou).order_by(Hangzhou.count.desc()).all()
    elif city == "香港":
        data = db.session.query(Hongkong).order_by(Hongkong.count.desc()).all()
    else:
        return json.dumps(view_data, ensure_ascii=False)

    view_data["series_data"] = []
    def build_view_data(item):
        tmp_dic = {}
        tmp_dic["price"] = item.count
        tmp_dic["city"] = item.ent
        view_data["series_data"].append(tmp_dic)

    for i in range(6):
        build_view_data(data[i])

    return json.dumps(view_data, ensure_ascii=False)


@data.route('/cityCountWho/<who>', methods=['GET'])
def city_count_who(who):
    print("enter data")
    print(who)
    view_data = {}
    if who == "和朋友":
        data = db.session.query(Friend).order_by(Friend.count.desc()).all()
    elif who == "亲子":
        data = db.session.query(Child).order_by(Child.count.desc()).all()
    elif who == "夫妻":
        data = db.session.query(Couple).order_by(Couple.count.desc()).all()
    elif who == "一个人":
        data = db.session.query(Alone).order_by(Alone.count.desc()).all()
    elif who == "情侣":
        data = db.session.query(Lover).order_by(Lover.count.desc()).all()
    elif who == "和父母":
        data = db.session.query(Parent).order_by(Parent.count.desc()).all()
    else:
        return json.dumps(view_data, ensure_ascii=False)

    view_data["series_data"] = []
    def build_view_data(item):
        tmp_dic = {}
        tmp_dic["price"] = item.count
        tmp_dic["city"] = item.city
        view_data["series_data"].append(tmp_dic)

    for i in range(6):
        build_view_data(data[i])

    return json.dumps(view_data, ensure_ascii=False)
