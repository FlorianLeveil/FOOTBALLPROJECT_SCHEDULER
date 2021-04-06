#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LEVEIL FLORIAN Enterprise, all rights reserved.

from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.secret_key = b'T\xee\xc2\xc3&\xb2\xd5\x8e;\xe9\xe4B\xdc?\xbe)'
app.config['MONGODB_SETTINGS'] = {
    'db': 'scheduler',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

# Database
# db.connect('my_db', host='127.0.0.1', port=27017)
from user import routes
from player import routes

# Routes
@app.route('/')
def home():
    return "Home"