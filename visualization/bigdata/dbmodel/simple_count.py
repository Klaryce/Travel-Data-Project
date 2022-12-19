from config import db


class CityCount(db.Model):
    __tablename__ = "city_count"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class DaysCount(db.Model):
    __tablename__ = "days_count"
    id = db.Column(db.Integer, primary_key=True)
    days = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class MoneyCount(db.Model):
    __tablename__ = "money_count"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.VARCHAR(45))
    money = db.Column(db.Integer)
    count = db.Column(db.INTEGER)
    ave = db.Column(db.Integer)

class MonthCount(db.Model):
    __tablename__ = "month_count"
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class WhoCount(db.Model):
    __tablename__ = "who_count"
    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class EntCount(db.Model):
    __tablename__ = "ent_count"
    id = db.Column(db.Integer, primary_key=True)
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class TrafficCount(db.Model):
    __tablename__ = "traffic_count"
    id = db.Column(db.Integer, primary_key=True)
    traffic = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class AccomCount(db.Model):
    __tablename__ = "accom_count"
    id = db.Column(db.Integer, primary_key=True)
    accom = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class TourCount(db.Model):
    __tablename__ = "tour_count"
    id = db.Column(db.Integer, primary_key=True)
    tour = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)
