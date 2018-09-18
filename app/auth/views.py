# -*- coding: utf-8 -*-
__author__ = '51439'

from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from .import auth
from ..models import UserInfo
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,PasswordResetRequestForm,PasswordResetForm
from .. import db
from ..email import send_mail




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserInfo.query.filter_by(Email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('用户名密码不正确')
    return render_template('auth/login.html',form=form)

@auth.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        userinfo = UserInfo(Email=form.email.data,UserName=form.username.data,
                            password=form.password.data)
        db.session.add(userinfo)
        db.session.commit()
        token = userinfo.generate_confirmation_token()
        send_mail(userinfo.Email,'确认你的账户','auth/email/confirm',userinfo=userinfo,token=token)
        flash('确认邮件已发送到你的邮箱')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经确认账号,谢谢！')
    else:
        flash('该验证链接无效或已过期！')
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出')
    return  redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed\
            and request.endpoint[:5]!='auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/changepassword',methods=['GET','POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            db.session.commit()
            flash('你已经成功修改密码！')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误，请重新输入！')
    return render_template('auth/changepassword.html',form = form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form=PasswordResetRequestForm()
    if form.validate_on_submit():
        user = UserInfo.query.filter_by(Email = form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_mail(user.Email,'重置密码','auth/email/resetpassword',user = user,token=token)
        flash('一封重置密码的确认邮件已经发送到您的邮箱，请确认！')
        return redirect(url_for('auth.login'))
    return render_template('auth/restpassword.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if UserInfo.reset_password(token,form.password.data):
            db.session.commit()
            flash('重置密码成功')
            return redirect(url_for('auth.login'))
        else:
            return  redirect(url_for('main.index'))
    return render_template('auth/restpassword.html',form=form)



