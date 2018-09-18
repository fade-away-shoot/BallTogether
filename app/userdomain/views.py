# -*- coding: utf-8 -*-
__author__ = '51439'

from . import userdomain
from flask import render_template, abort, flash, redirect, url_for, request
from ..models import UserInfo
from .forms import UserInfoForm, UserImageForm
from .. import db
import os
from werkzeug.utils import secure_filename
from flask_login import current_user,login_required


@userdomain.route('/usermain/<username>')
@login_required
def usermain(username):
    user = UserInfo.query.filter_by(UserName=username).first_or_404()
    img_url = '/static/image/' + user.UserName + '.jpg'
    dicfollowed={}
    for followed_user in user.followed.all():
        dicfollowed[followed_user.followed.UserName] = '/static/image/' + followed_user.followed.UserName + '.jpg'
    dicfollower = {}
    for follower_user in user.followers.all():
        dicfollower[follower_user.follower.UserName] = '/static/image/' + follower_user.follower.UserName + '.jpg'
    basepath = os.getcwd()
    upload_path = os.path.join(basepath, 'app\\static\\image', secure_filename(user.UserName + '.jpg'))
    if not os.path.exists(upload_path):
        img_url = '/static/image/default.jpg'
    if current_user.is_authenticated and user == current_user:
        html_url = 'userdomain/usermain.html'
    else:
        html_url = 'userdomain/otherusermain.html'
    return render_template(html_url, user=user, img_url=img_url,dicfollowed = dicfollowed,dicfollower=dicfollower)


@userdomain.route('/useredit/<username>', methods=['GET', 'POST'])
@login_required
def useredit(username):
    form = UserInfoForm()
    user = UserInfo.query.filter_by(UserName=username).first_or_404()
    if not current_user.is_authenticated or user != current_user:
        return redirect(url_for('userdomain.usermain'))
    if form.validate_on_submit():
        user.Location = form.location.data
        user.PhoneNum = form.phonenumber.data
        user.ShowPhoneNum = form.showphonenum.data
        user.PlayFre = form.playfre.data
        user.OftenTime = form.oftentime.data
        user.OftenWhere = form.oftenwhere.data
        db.session.add(user)
        db.session.commit()
        flash('保存成功！')
        return redirect(url_for('userdomain.useredit', username=user.UserName))
    form.location.data = user.Location
    form.phonenumber.data = user.PhoneNum
    form.showphonenum.data = user.ShowPhoneNum
    form.playfre.data = user.PlayFre
    form.oftentime.data = user.OftenTime
    form.oftenwhere.data = user.OftenWhere
    img_url = '/static/image/' + user.UserName + '.jpg'
    basepath = os.getcwd()
    upload_path = os.path.join(basepath, 'app\\static\\image', secure_filename(user.UserName + '.jpg'))
    if not os.path.exists(upload_path):
        img_url = '/static/image/default.jpg'
    return render_template('userdomain/userinfoedit.html', form=form, img_url=img_url)


@userdomain.route('/useredit/userimg/<username>', methods=['GET', 'POST'])
@login_required
def userimg(username):
    form = UserImageForm()
    user = UserInfo.query.filter_by(UserName=username).first_or_404()
    if not current_user.is_authenticated or user != current_user:
        return redirect(url_for('userdomain.usermain'))
    img_url = '/static/image/' + user.UserName + '.jpg'
    basepath = os.getcwd()
    upload_path = os.path.join(basepath, 'app\\static\\image', secure_filename(user.UserName + '.jpg'))
    if not os.path.exists(upload_path):
        img_url = '/static/image/default.jpg'
    if form.validate_on_submit():
        f = request.files["imgfile"]
        f.filename=user.UserName+'.jpg'
        basepath = os.getcwd()
        upload_path = os.path.join(basepath, 'app\\static\\image', secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for('userdomain.userimg',username=user.UserName))
    return render_template('userdomain/userimage.html', form=form, img_url=img_url)

@userdomain.route('/follow/<username>')
@login_required
def follow(username):
    user = UserInfo.query.filter_by(UserName = username).first()
    if user is None:
        flash('该用户(' + username + ')不存在!')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已关注过该用户！')
        return redirect(url_for('userdomain.usermain',username=username))
    current_user.follow(user)
    flash('关注成功！')
    return redirect(url_for('userdomain.usermain',username=username))



@userdomain.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = UserInfo.query.filter_by(UserName=username).first()
    if user is None:
        flash('该用户('+username+')不存在!')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('你并没有关注该用户！')
        return redirect(url_for('userdomain.usermain',username=username))
    current_user.unfollow(user)
    flash('取消关注成功！')
    return redirect(url_for('userdomain.usermain',username=username))

