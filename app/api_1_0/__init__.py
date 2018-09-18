# -*- coding: utf-8 -*-
__author__ = '51439'

from flask import Blueprint

api = Blueprint('api',__name__)

from . import errors


