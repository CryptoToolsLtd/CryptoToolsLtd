from flask import Flask
from .api.jobs.worker import start_worker_pool
from flask_login import LoginManager # type: ignore
from flask_migrate import Migrate
from .models import db

from app.env import (
    MYSQL_HOSTNAME, MYSQL_HOSTPORT,
    MYSQL_USERNAME, MYSQL_PASSWORD,
    MYSQL_DATABASE,SECRET_KEY
)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:{MYSQL_HOSTPORT}/{MYSQL_DATABASE}"
    db.init_app(app)
    
    migrate = Migrate(app, db) # type: ignore
    
    from .views import views
    from .auth import auth
    from .api import api
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(api,url_prefix='/api')
    
    from .models import User
    
    # create_database(app) 
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # type: ignore
    login_manager.init_app(app) # type: ignore
    
    @login_manager.user_loader # type: ignore
    def load_user(id: int): # type: ignore
        return User.query.get(int(id))
    
    start_worker_pool(app)
    
    return app

# def create_database(app):
#     if not path.exists('app/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created database!')
