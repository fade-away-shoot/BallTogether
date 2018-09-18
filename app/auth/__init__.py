# -*- coding: utf-8 -*-
__author__ = '51439'

from flask import Blueprint

auth = Blueprint('auth',__name__)

from .import views