import datetime
from energy_system import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    meter_id=db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False) 
    auth_code = db.Column(db.String(10), nullable=False,default='101')
    meter_uses = db.relationship('Meter_Data', backref='Consumer', lazy=True)

    def __repr__(self):
        return f"User('{self.name}','{self.meter_id}', '{self.email}','{self.phone}','{self.address}', '{self.image_file}'"
   
class Meter_Data(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    submit_id =  db.Column(db.String(30), nullable=False)
    meter_kwh = db.Column(db.String(1000), nullable=False)
    submit_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    
    def __repr__(self):
        return f"Meter_Data('{self.submit_id}','{self.meter_kwh}', '{self.submit_time}')"