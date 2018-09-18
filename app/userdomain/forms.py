# -*- coding: utf-8 -*-
__author__ = '51439'
from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,FileField
from wtforms.validators import Required


class UserInfoForm(FlaskForm):
    location = StringField('所在地')
    localpoint = StringField('常驻点',)
    phonenumber = StringField('手机号码')
    showphonenum = BooleanField('是否显示手机号码')
    playfre = StringField('打球频次')
    oftentime = StringField('常打球时间')
    oftenwhere = StringField('常打球球场')
    submit = SubmitField('保存')

class UserImageForm(FlaskForm):
    imgfile = FileField('上传新头像',validators=[Required()])
    submit = SubmitField('上传新头像')