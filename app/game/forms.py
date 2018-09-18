# -*- coding: utf-8 -*-
__author__ = '51439'

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateTimeField, SelectField, RadioField,SelectMultipleField,IntegerField,TextAreaField
from wtforms.validators import InputRequired


# 创建约球表单
class CreateTeamForm(FlaskForm):
    title = StringField('约球简要', validators=[InputRequired()])
    groundid = StringField('选择球场', validators=[InputRequired()])
    playtime = DateTimeField('集合时间', validators=[InputRequired()])
    playtype = RadioField('约球范围', validators=[InputRequired()], choices=[('0','所有人'), ('1','粉丝和关注')])
    needman = IntegerField('召集人数', validators=[InputRequired()])
    money = StringField('份子钱', validators=[InputRequired()])
    wantman = SelectField('十分，非常想要', validators=[InputRequired()],
                                  choices=[('0','风骚运球怪'), ('1','无解强投手'), ('2','勾手老大爷'), ('3','灵活死胖子'), ('4','内线大肌霸'), ('5','滞空弹跳男'), ('6','各位大哥，我包水，管够')])
    playinfo=TextAreaField('领导说两句',)
    submit=SubmitField('发布')

