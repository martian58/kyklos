from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    phone_number = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=False)
    binance_api_key = db.Column(db.String(256))
    binance_secret_key = db.Column(db.String(256))
    role = db.Column(db.String(20), default="user")

    def __repr__(self) -> str:
        return f"{self.uid} : {self.username}"
    

    def get_id(self):
        return self.uid