# -*- coding:utf-8 -*-
from flask import Blueprint, render_template
from config import db
from .form import CityForm, WhoForm
from dbmodel.city_recommend import CityRecommand
from dbmodel.who_recommend import WhoRecommand

"""
本视图专门用于处理页面
"""
page = Blueprint('page', __name__)


@page.route('/', endpoint="index")
def login():
    return render_template("index.html")


@page.route('/city_recommend/<city>', methods=['GET','POST'])
def city_recommend(city):
    city_info = db.session.query(CityRecommand).filter_by(city=city).first()
    return render_template('city_recommend.html', city_info=city_info)


@page.route('/who_recommend/<who>', methods=['GET','POST'])
def who_recommend(who):
    print("page")
    print(who)
    who_info = db.session.query(WhoRecommand).filter_by(who=who).first()
    return render_template('who_recommend.html', who_info=who_info)
