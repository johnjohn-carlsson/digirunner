from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    Token = db.Column(db.String(50), unique=False, nullable=False)
    Username = db.Column(db.String(50), unique=False, nullable=False)
    Email = db.Column(db.String(50), unique=False, nullable=False)
    Password = db.Column(db.String(400), unique=False, nullable=False)  # Increased length for hashed password
    ActiveRoute = db.Column(db.String(100), unique=False, nullable=True)
    ActiveRouteMeters = db.Column(db.Integer, unique=False, nullable=True)
    TotalRanMeters = db.Column(db.Integer, unique=False, nullable=True)

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

def save_to_db(dictionary):

    u = User()
    u.Token = dictionary["Token"]
    u.Username = dictionary["Username"]
    u.Email = dictionary["Email"]
    u.set_password(dictionary["Password"])
    u.ActiveRoute = "None"
    u.ActiveRouteMeters = 0
    u.TotalRanMeters = 0

    db.session.add(u)
    db.session.commit()


def fetch_user(username):

    user = User.query.filter_by(Username=username).first()

    if user:
        return user
    
    return False

def update_amount_ran(username, length):

    user:User = User.query.filter_by(Username=username).first()

    if user:
        user.TotalRanMeters += float(length) * 1000
        user.ActiveRouteMeters += float(length) * 1000

        db.session.commit()

def update_selected_route(username, map:str):

    map = map.replace("_"," ").title()
    user:User = User.query.filter_by(Username=username).first()

    if user:
        user.ActiveRoute = map
        user.ActiveRouteMeters = 0

        db.session.commit()

        map_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images', 'usermaps', f"{username}_updated_map.jpg")
        
        # Check if the file exists, and if so, delete it
        if os.path.exists(map_image_path):
            os.remove(map_image_path)

def fetch_leaderboard() -> list:

    users = User.query.order_by(User.TotalRanMeters.desc()).limit(10).all()
    return users