from cmath import log
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = 'static/uploads/'

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fgjkldfgjkldfgljkfdgjkl fgfd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)

    from .viewsAdmin import viewsAdmin
    from .viewsClient import viewsClient
    from .authAdmin import authAdmin

    app.register_blueprint(viewsAdmin, url_prefix='/')
    app.register_blueprint(viewsClient, url_prefix='/')
    app.register_blueprint(authAdmin, url_prefix='/')

    from .models import UserAdmin, Service, Gallery

    create_database(app)
    with app.app_context():      
        if(db.session.query(UserAdmin).count() <= 0):
            new_user = UserAdmin(email= 'dtcong@gmail.com', password=generate_password_hash('12345678', method='sha256'))
            db.session.add(new_user)
            db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'authAdmin.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return UserAdmin.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Create Database!')
