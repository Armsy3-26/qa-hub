from time import time
import jwt
from  qa import db
import datetime
from flask_login  import UserMixin
from qa import login, app

@login.user_loader
def load_user(id):
    
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    
    __tablename__  = 'user'
    
    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username  =  db.Column(db.String(20), unique=True, nullable=False)
    email   =  db.Column(db.String(50), unique=True, nullable=False)
    password  =  db.Column(db.String(1900), nullable=False)
    date_joined  = db.Column(db.DateTime, default=datetime.datetime.now)
    image_file   =  db.Column(db.String, default="armsy.jpg")
    bio       =  db.Column(db.String, default="QA-Hub we got fuck!")
    question  =  db.relationship('Question', backref='owner')
    answer  =  db.relationship('Answer', backref='owner')
    comment =  db.relationship('Comment', backref='owner')
    
    def get_pass_reset_token(self):
        return jwt.encode(
            {'reset_pass': self.id, 'exp': 600},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_pass_token(token):
        
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
        except:
            
            return 
        return User.query.get(id)
    
    def __repr__(self):
        
        return f"Username: {self.username} :: Email: {self.email}"

class Question(db.Model):
    
    __tablename__  =  'question'
    
    id    =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    questions   =  db.Column(db.String)
    datetime_posted  =  db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    question  =  db.relationship('Answer', backref='question')
    user_id   =  db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def  __repr__(self):
        
        return f"Question: {self.question}  \n Answer: {self.answer}" 
    
class Answer(db.Model):
    
    __tablename__ = 'answer'
    
    id = db.Column(db.Integer, primary_key=True)
    answers   =  db.Column(db.String)
    datetime_posted  =  db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    question_id   =  db.Column(db.Integer, db.ForeignKey('question.id'))
    answer   =  db.relationship('Comment', backref="answer")
    user_id   =  db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        
        return '{}'.format(self.answer)
    
class Comment(db.Model):
    
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    comment   =  db.Column(db.String)    
    datetime_posted  =  db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    answer_id   =  db.Column(db.Integer, db.ForeignKey('answer.id'))
    user_id   =  db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        
        return '{}'.format(self.answer)
    

    