import os
from  flask import Flask
from  flask_sqlalchemy  import SQLAlchemy
from flask_login  import LoginManager
from flask_mail  import Mail


app  =  Flask(__name__, 
              template_folder="templates",
              static_folder="static"
              )
app.config['SECRET_KEY'] = '1234QWERTTY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///qa.db'
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'armstrongnyagwencha41@gmail.com',
    MAIL_PASSWORD = 'armstrong41',
))
app.config['UPLOAD_FOLDER']  = "members"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

login  =  LoginManager(app)
login.login_view = 'login'

db  =  SQLAlchemy(app)

mail = Mail(app)


from qa  import routes