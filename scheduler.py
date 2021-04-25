#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LEVEIL FLORIAN Enterprise, all rights reserved.

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from database import db
from game_manager.GameManager import GameManager


def create_app():
    app = Flask(__name__)
    # REDIS_URL = "redis://:password@localhost:6379/0"
    app.secret_key = b'T\xee\xc2\xc3&\xb2\xd5\x8e;\xe9\xe4B\xdc?\xbe)'
    app.config['MONGODB_SETTINGS'] = {
        'db'  : 'scheduler',
        'host': '127.0.0.1',
        'port': 27017
    }
    db.init_app(app)
    app.config["JWT_SECRET_KEY"] = b'T\xee\xc2\xc3&\xb2\xd5\x8e;\xe9\xe4B\xdc?\xbe)'
    jwt = JWTManager(app)
    redis_client = FlaskRedis(app)
    redis_client.flushdb()
    return redis_client, app


redis_client, app = create_app()
app.run()
game_manager = GameManager(redis_client)

# ROUTES
from user import routes
from player import routes
from game_manager import routes
