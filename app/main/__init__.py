# -*- coding: utf-8 -*-
__author__ = '51439'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
