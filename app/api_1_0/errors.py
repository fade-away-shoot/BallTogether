# -*- coding: utf-8 -*-
__author__ = '51439'
from flask import jsonify


def forbidden(message):
    reponse = jsonify({'error': 'forbidde', 'message': message})
    reponse.status_code = 403
    return reponse


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response
