# -*-coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, BooleanField,  TextAreaField, SelectMultipleField, SelectField, PasswordField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from dbmodel.simple_count import CityCount, DaysCount, MoneyCount, MonthCount, TrafficCount, EntCount, WhoCount


cities = ["三亚", "成都", "丽江", "厦门", "杭州", "香港"]
who = ["和朋友", "亲子", "夫妻", "一个人", "情侣", "和父母"]


class CityForm(Form):
    city = SelectField('city', choices=cities, validators=[DataRequired()])


class WhoForm(Form):
    who = SelectField('who', choices=who, validators=[DataRequired()])