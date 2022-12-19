from config import db


class WhoRecommand(db.Model):
    __tablename__ = "recommend_who"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    who = db.Column(db.VARCHAR(45))
    days = db.Column(db.VARCHAR(45))
    month = db.Column(db.VARCHAR(45))
    money = db.Column(db.INTEGER)
    ent = db.Column(db.VARCHAR(45))

class Friend(db.Model):
    __tablename__ = "city_count_friend"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(50))
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)


class Child(db.Model):
    __tablename__ = "city_count_child"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(50))
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Couple(db.Model):
    __tablename__ = "city_count_couple"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(50))
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Alone(db.Model):
    __tablename__ = "city_count_alone"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(50))
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Lover(db.Model):
    __tablename__ = "city_count_lover"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(50))
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)


class Parent(db.Model):
    __tablename__ = "city_count_parent"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(50))
    who = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)
