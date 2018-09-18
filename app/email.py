# -*- coding: utf-8 -*-
__author__ = '51439'
from . import mail
from flask_mail import Message

from flask import render_template



def send_mail(to,subject,template,**kwargs):
    msg = Message('[一起约球]'+subject,
                    sender='zouyu<514399533@qq.com>',recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    mail.send(msg)
