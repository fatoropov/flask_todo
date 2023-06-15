import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()
app = Flask(__name__)
bootstrap.init_app(app)
moment.init_app(app)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or \
                            "thisisjustfordevelopment"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


from app import routes

with app.app_context():
    db.create_all()
