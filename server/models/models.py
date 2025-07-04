from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    pin_code = db.Column(db.String(10))
    vehicle_number = db.Column(db.String(20))
    contact_number = db.Column(db.String(20))
    role = db.Column(db.String(10), default='user')  # 'admin' or 'user'

    records = db.relationship('ParkingRecord', backref='user', lazy=True, cascade="all, delete-orphan")

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    lot_id = db.Column(db.Integer, primary_key=True)
    lot_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade="all, delete-orphan")

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    spot_id = db.Column(db.String, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.lot_id'), nullable=False)
    status = db.Column(db.String(1), default='A')  # A = Available, O = Occupied

    record = db.relationship('ParkingRecord', backref='spot', lazy=True, cascade="all, delete-orphan")

class ParkingRecord(db.Model):
    __tablename__ = 'parking_records'
    record_id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.spot_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(1), default='O')
    # add a field here which shows if it is ongoing or closed parking
    # and makes changes to filtering in the get spot details for getting records
