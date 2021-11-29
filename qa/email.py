#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 22:03:38 2021

@author: armsy326
"""
from flask import render_template
from flask_mail import Message
from qa  import mail



def send_mail(subject, sender, receipents, text_body, html_body):
    
    msg  =  Message(subject, sender=sender, recipients=receipents)
    
    msg.body  =  text_body
    msg.html  =  html_body
    
    mail.send(msg)
    
def send_pass_reset_email(user):
    token  =  user.get_pass_reset_token()
    send_mail('[QA-Hub] Reset Your Password',
              sender = 'armstrongnyagwencha41@gmail.com',
              receipents = [user.email],
              text_body=render_template('email/reset_password.txt', user=user, token=token),
              html_body = render_template('email/reset_password.html',
                                          user=user, token=token))