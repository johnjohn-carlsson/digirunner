from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    Token = db.Column(db.String(50), unique=False, nullable=False)
    Username = db.Column(db.String(50), unique=False, nullable=False)
    Email = db.Column(db.String(50), unique=False, nullable=False)
    Password = db.Column(db.String(400), unique=False, nullable=False)  # Increased length for hashed password
    ActiveRoute = db.Column(db.String(100), unique=False, nullable=True)
    TotalRanKMS = db.Column(db.Integer, unique=False, nullable=True)

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
    u.TotalRanKMS = 0

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
        user.TotalRanKMS += int(length)

        db.session.commit()

def update_selected_route(username, map):

    user:User = User.query.filter_by(Username=username).first()

    if user:
        user.ActiveRoute = map

        db.session.commit()