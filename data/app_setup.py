# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
#
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'db/main.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# with app.app_context():
#     db.create_all()