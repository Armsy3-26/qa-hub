#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:53:08 2021

@author: armsy326
"""
import os
from  flask import Flask
from flask  import render_template, url_for, redirect, flash, request
from werkzeug.utils import secure_filename
from werkzeug.security  import check_password_hash, generate_password_hash
from qa.models  import User, Question, Answer, Comment
from qa import app, db
from qa.forms import QuestionForm, RegisterForm, LoginForm, ResetPasswordForm1, ResetPasswordForm, AnswerForm
from flask_login  import login_required, login_user, current_user, logout_user
from qa.email  import send_pass_reset_email


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':

        form  =  AnswerForm()

        key  =  request.form['value']

        return render_template('main.html', question = "What is intel 1886 architecture? state 2 properties acculuataing to its nowing budgtsj", form=form)
        
    return render_template('index.html')

##contribution route snippet

@app.route('/contribute', methods=['POST', 'GET'])
def contribute():
    
    if request.method == 'POST':
        
        question  =  request.values['question']
        
        answer   =  request.values['answer']
        
        quiz   =  Question(questions=question, owner=current_user)
        
        ans  =  Answer(answers=answer, owner=current_user, question=question)
        
        db.session.add(quiz)
        
        db.session.add(ans)
        
        db.session.commit()
    
    return render_template("contribute.html", title="contribute to qa-hub")

@app.route('/register', methods=['GET', 'POST'])
def register():

    form  =  RegisterForm()
    
    if form.validate_on_submit():
        
        username  =  form.username.data
        email  =  form.email.data
        password  = form.password.data
        
        enct_pass  =  generate_password_hash(password)
        
        user  =  User(username=username, email=email, password=enct_pass)
        
        db.session.add(user)
        
        db.session.commit()
        
        flash("Welcome to QA-Hub you can post, answer a question or comment")
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form = form, title="Register to QA-Hub")
        
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        
        return redirect(url_for('index'))
    
    form =  LoginForm()
    
    if form.validate_on_submit():
        
     
        user =  User.query.filter_by(username=form.username.data).first()
        
        if user is None or not  check_password_hash(user.password, form.password.data):
            flash("Invalid password or username, Try again")
            return redirect(url_for('login'))
        next_page  =  request.args.get('next')
        login_user(user , remember=form.remember.data)
        return redirect(next_page) if next_page else redirect(url_for('index'))
        
            
    return render_template('login.html', form = form, title="login to QA-Hub")


@app.route('/askquestion')
@login_required
def askquestion():
    
    form  = QuestionForm()
    
    if form.validate_on_submit():
        
        question  =  form.question.data
        
        quiz  =  Question(questions=question)
        
        db.session.add(quiz)
        
        db.session.commit()
        
        flash("Your question has been submitted successfully")
        
        return redirect(url_for('index'))
        
    return render_template('askquestion.html', title="ask question in QA-Hub", form=form)

    
@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    
    query_date   =  User.query.filter_by(date_joined=current_user.date_joined).first()

    date_joined =  query_date.date_joined.strftime('%Y-%m-%d  %H:%M:%S')

    image  =  os.path.abspath('qa/templates/static/Gavinixbreexy.jpg')
    
    return render_template('account.html', title="user account", date_joined=date_joined, image=image)

@app.route('/reset_pass_request', methods=['POST', 'GET'])
def reset_pass_request():

    if current_user.is_authenticated:

        return redirect(url_for('index'))

    form = ResetPasswordForm1()
    
    if form.validate_on_submit():
        
        user =  User.query.filter_by(email=form.email.data).first()
        
        if user:
            
            send_pass_reset_email(user)
            
        flash("Check your email for futher instructions to reset your password")
        
        return redirect(url_for('login'))
            

    return render_template('reset_pass_request.html', title="Requesting for password reset", form=form)

@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    
    if current_user.is_authenticated:
        return redirect(url_for(index))
    
    user  = User.verify_reset_pass_token(token)
    
    if not user:
        
        return redirect(url_for('index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        
        user.generate_password_hash(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form, title="Reset password")
    
@app.route('/profile_update', methods=['POST', 'GET'])
@login_required
def profile_update():
    
    if request.method == 'POST':
        
        username  =  request.values['username']
        bio    =  request.values['bio']
        
        image_file  =  request.files['file']
        
        if username == '':
            current_user.username = current_user.username
        else:
            current_user.username = username
        if bio == '':
            current_user.bio = current_user.bio
        else:
            current_user.bio = bio
        if image_file == '':
            current_user.image_file  =  current_user.image_file
        else:
            
            file_name = secure_filename(current_user.username + image_file.filename )
            
            image_file.save(secure_filename(current_user.username + image_file.filename ))
            
            current_user.image_file = file_name
        
        db.session.commit()
        
        
        
        return redirect(url_for('account'))
        
        
    
    
    return render_template('profile_update.html', title="profile update", )

@app.route('/logout')

def logout():
    
    logout_user()
    
    return redirect(url_for('index'))
