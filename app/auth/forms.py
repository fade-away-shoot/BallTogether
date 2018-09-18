# -*- coding: utf-8 -*-
__author__ = '51439'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, InputRequired, EqualTo, ValidationError
from ..models import UserInfo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(1, 50), Email()])
    password = PasswordField('密码', validators=[InputRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(1, 50), Email("请输入正确的邮箱地址")])
    username = StringField('用户名', validators=[InputRequired(), Length(1, 50), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                     '用户名必须为字母、数字、点或下划线')])
    password = PasswordField('密码', validators=[InputRequired(), EqualTo('password2', '两次密码输入不一致，请重新输入'),
                                               Regexp('^[A-Za-z][A-Za-z0-9][A-Za-z0-9_.]*$', 0,
                                                      '密码必须为字母、数字、点或下划线')])
    password2 = PasswordField('再次输入密码', validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9][A-Za-z0-9_.]*$', 0,
                                                                            '密码必须为字母、数字、点或下划线')])

    submit = SubmitField('注册')

    # 校验邮箱是否注册
    def validate_email(self, field):
        if UserInfo.query.filter_by(Email=field.data).first():
            raise ValidationError('邮箱地址已被注册！')

    # 校验用户名是否被使用
    def validate_username(self, field):
        if UserInfo.query.filter_by(UserName=field.data).first():
            raise ValidationError('用户名已被使用！')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('原密码', validators=[InputRequired()])
    newpassword = PasswordField('新密码', validators=[InputRequired(), EqualTo('confirmpassword', '两次密码输入不一致，请重新输入'),
                                                   Regexp('^[A-Za-z][A-Za-z0-9][A-Za-z0-9_.]*$', 0,
                                                          '密码必须为字母、数字、点或下划线')])
    confirmpassword = PasswordField('确认新密码',
                                    validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9][A-Za-z0-9_.]*$', 0,
                                                                        '密码必须为字母、数字、点或下划线')])
    submit = SubmitField('确认修改')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('E-Mail', validators=[InputRequired(), Length(1, 50), Email("请输入正确的邮箱地址")])
    submit = SubmitField('发送重置密码邮件')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[InputRequired(), EqualTo('confirmpassword', '两次密码输入不一致，请重新输入'),
                                                Regexp('^[A-Za-z][A-Za-z0-9][A-Za-z0-9_.]*$', 0,
                                                       '密码必须为字母、数字、点或下划线')])
    confirmpassword = PasswordField('确认新密码',
                                    validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9][A-Za-z0-9_.]*$', 0,
                                                                        '密码必须为字母、数字、点或下划线')])
    submit=SubmitField('确认重置密码')
