from flask_wtf  import FlaskForm
from wtforms.validators import Email,DataRequired, EqualTo, Length, ValidationError
from wtforms  import StringField, SubmitField, PasswordField, BooleanField, SelectField
from  qa.models  import User



class QuestionForm(FlaskForm):
    fields  =  ['nursing', 'Computer Science', 'information Technology', 'cybersecurity', 'hosipitality']
    question  =  StringField('question', validators=[DataRequired()])
    field     =  SelectField('Field', choices=fields)
    submit   =  SubmitField('Submit')
    
class AnswerForm(FlaskForm):
    answer     =  StringField('answer', validators=[DataRequired()], render_kw={'style': 'height: 30ch'})
    submit   =  SubmitField('Submit')
    
class RegisterForm(FlaskForm):

    username  =  StringField('Username', validators=[DataRequired(), Length(min=4, max=15)])
    email   =  StringField('Email', validators=[DataRequired(), Email(message="Enter a valid email")])
    password  =  PasswordField('Password', validators=[DataRequired()])
    confirm_password  =  PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'),])
    submit   =  SubmitField('Submit')
    
    
    def validateusername(self, username):
        
        user   =  User.query.filter_by(username=username.data).first()
        
        if user:
            
            raise ValidationError("Username already exists")
            
    def validateemail(self, email):
        
        email  =  User.query.filter_by(email=email.data).first()
        
        if email:
            
            raise ValidationError("Email already exists")
            
class LoginForm(FlaskForm):
    
    username  =  StringField('Username', validators=[DataRequired()])
    password  =  PasswordField('Password', validators=[DataRequired()])
    remember  =  BooleanField('Remember Me')
    submit   =  SubmitField('Submit')
    
    
class ResetPasswordForm1(FlaskForm):
    
    email  =  StringField('Email', validators=[DataRequired(), Email()])
    submit   =  SubmitField('Password Reset')
    
class ResetPasswordForm(FlaskForm):
    
    password  =  PasswordField('Password', validators=[DataRequired()])
    password2  =  PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit  = SubmitField('Reset Password')
    
    