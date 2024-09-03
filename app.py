from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate, upgrade
from database import db
from routes.index import indexBluePrint
from routes.maps import mapsBluePrint
from routes.login import loginBluePrint
from routes.register import registerBluePrint
from routes.profile import profileBluePrint
from database import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superfuckingsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/digirunner'

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):   
    return User.query.get(int(user_id))

app.register_blueprint(indexBluePrint)
app.register_blueprint(mapsBluePrint)
app.register_blueprint(registerBluePrint)
app.register_blueprint(loginBluePrint)
app.register_blueprint(profileBluePrint)

if __name__ == '__main__':
    with app.app_context():
        upgrade()

    app.run(debug=True)
