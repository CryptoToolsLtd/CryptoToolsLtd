from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

from utils.env import (
    MYSQL_HOSTNAME, MYSQL_HOSTPORT,
    MYSQL_USERNAME, MYSQL_PASSWORD,
    MYSQL_DATABASE,SECRET_KEY
)


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:{MYSQL_HOSTPORT}/{MYSQL_DATABASE}"
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    from .views import views
    from .auth import auth
    from .api import api
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(api,url_prefix='/api')
    
    from .models import User
    
    # create_database(app) 
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def  load_user(id):
        return User.query.get(int(id))
    
    return app

# def create_database(app):
#     if not path.exists('app/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created database!')
