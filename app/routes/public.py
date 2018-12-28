#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
from sanic import Blueprint
from sanic.response import text

logger = logging.getLogger(__name__)
public_pb = Blueprint('public')


@public_pb.route('/')
def index(request):
    return text('It works.')


@public_pb.route('/error')
def error(request):
    raise ValueError('This is a ValueError!')


@public_pb.route('/log_error')
def log_error(request):
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.error(f'This is a log error, exp:{e}!', exc_info=True)
    return text('This is log_error!')
