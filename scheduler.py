#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LEVEIL FLORIAN Enterprise, all rights reserved.

from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis

from game.game import Game
from game_manager.GameManager import GameManager
# from player.player import Player

app = Flask(__name__)
REDIS_URL = "redis://:password@localhost:6379/0"
app.secret_key = b'T\xee\xc2\xc3&\xb2\xd5\x8e;\xe9\xe4B\xdc?\xbe)'
app.config['MONGODB_SETTINGS'] = {
    'db'  : 'scheduler',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
app.config["JWT_SECRET_KEY"] = b'T\xee\xc2\xc3&\xb2\xd5\x8e;\xe9\xe4B\xdc?\xbe)'
jwt = JWTManager(app)
redis_client = FlaskRedis(app)


# game_manager = GameManager(redis_client, db)
# Database
# db.connect('my_db', host='127.0.0.1', port=27017)

# from user import routes
# from player import routes
#

# my_dict = {"toto" : 2, "tata": 15}
# redis_client.hmset('user',my_dict)
# print(redis_client.hgetall('user'))
# redis_client.hmset('user',{"toto" : 12})
# print(redis_client.hgetall('user'))
#
# toto = redis_client.hgetall('user')
# redis_client.hmset('user2', toto)
# print(redis_client.hgetall('user2'))
# redis_client.delete('user2')
# print("test")
# print(redis_client.hgetall('user2'))
#
# redis_client.delete('LanguageList')
#
# redis_client.lpush('LanguageList', "Kotlin")
# redis_client.lpush('LanguageList', "coucou")
#
# print(redis_client.llen('LanguageList'))
# i = 0
# while i != redis_client.llen('LanguageList'):
#     print(redis_client.lindex('LanguageList', i))
#     i += 1




# Routes
@app.route('/')
def home():
    return "Home"

# Gagner l'action attaque vs defense
#Attack
# age 10
# height 10
# overall 10
# agility 12
# dribbling 15
# balance 7
# ball_control 15
# sprint_speed 13
# acceleration 13
# crossing 7
#
# 112
# #defense
# age 10
# height 10
# overall 10
# agility 12
# dribbling 14
# interceptions 14
# marking 14
# standing_tackle 14
# sliding_tackle 14
#
# #choisir a qui passer
# vision
# strength
# short_passing
# long_passing
# positioning
#
# #Other
# penalties
# reactions
# aggression
