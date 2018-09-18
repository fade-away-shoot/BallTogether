# -*- coding: utf-8 -*-
__author__ = '51439'

from flask import Blueprint

userdomain = Blueprint('userdomain',__name__)

from . import views
