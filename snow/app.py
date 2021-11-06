# coding=utf-8

from flask import Flask
from flask_admin import Admin
from werkzeug.utils import import_string
from snow.views.index import IndexView
import flask_login as login
from snow.ext import db

import os

modelviews = ['snow.views.index.account_view', 'snow.views.gsc.gsc_view']

extensions = ['snow.ext.db']

login_manager = login.LoginManager()


def create_app():
    app = Flask('snow')
    app.config['SERVER_NAME'] = os.environ.get('SNOW_SERVER_NAME')
    app.config['SECRET_KEY'] = os.environ.get('SNOW_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SNOW_SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1440
    app.config['SQLALCHEMY_POOL_SIZE'] = 100
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
    admin = Admin(app, name='📚', template_mode='bootstrap4', base_template='base.html',
                  index_view=IndexView(url='/', name=''))
    login_manager.init_app(app)
    for extension in extensions:
        ext = import_string(extension)
        ext.init_app(app)
    for modelview_qualname in modelviews:
        modelview = import_string(modelview_qualname)
        admin.add_view(modelview)
    return app


@login_manager.user_loader
def load_user(user_id):
    from snow.models.account import Account
    return db.session.query(Account).get(user_id)