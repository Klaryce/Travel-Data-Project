from config import db


class CityRecommand(db.Model):
    __tablename__ = "recommend_city"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    who = db.Column(db.VARCHAR(45))
    days = db.Column(db.VARCHAR(45))
    month = db.Column(db.VARCHAR(45))
    money = db.Column(db.INTEGER)
    ent = db.Column(db.VARCHAR(45))


class Sanya(db.Model):
    __tablename__ = "ent_count_sanya"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Chengdu(db.Model):
    __tablename__ = "ent_count_chengdu"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Lijiang(db.Model):
    __tablename__ = "ent_count_lijiang"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Xiamen(db.Model):
    __tablename__ = "ent_count_xiamen"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Hangzhou(db.Model):
    __tablename__ = "ent_count_hangzhou"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)

class Hongkong(db.Model):
    __tablename__ = "ent_count_hongkong"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.VARCHAR(45))
    ent = db.Column(db.VARCHAR(45))
    count = db.Column(db.INTEGER)