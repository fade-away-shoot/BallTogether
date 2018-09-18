# -*- coding: utf-8 -*-
__author__ = '51439'

from datetime import datetime
from flask import render_template, session, redirect, url_for,abort

from . import main
from .forms import NameForm
from .. import db
from ..models import UserInfo
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

# @main.route('/user/<username>')
# def user(username):
#     user = UserInfo.query.filter_by(UserName = username).first()
#     if user is None:
#         abort(404)
#     return render_template('user.html',user = user)

@main.route('/map')
def map():
    return render_template('userdomain/map.html')