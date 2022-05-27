from email.policy import default
from enum import unique
from pytz import timezone
from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func

class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    def __ref__(self):
        return f"UserAdmin('{self.email}','{self.password}')"

class Service(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(600))
    name_img = db.Column(db.String(600))
    mimetype = db.Column(db.String(600))

    def __ref__(self):
        return f"Service('{self.name}','{self.description}','{self.mimetype}','{self.name_img}')"

class Gallery(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    img = db.Column(db.String(600))
    mimetype = db.Column(db.String(600))
    category = db.Column(db.Integer)

    def __ref__(self):
        return f"Service('{self.name}','{self.img}','{self.mimetype}','{self.category}')"