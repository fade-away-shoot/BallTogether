# -*- coding: utf-8 -*-
__author__ = '51439'

from flask import Blueprint

game = Blueprint('game',__name__)

from . import views