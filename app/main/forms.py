# -*- coding: utf-8 -*-
__author__ = '51439'

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('你是真的美腻，是吧？',validators=[Required()])
    submit = SubmitField('确认')