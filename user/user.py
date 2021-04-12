#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LeveilFlorian Enterprise, all rights reserved.

import json
import uuid
from _datetime import datetime

from flask import jsonify, request, session
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from player.player import Player
from scheduler import db

from operator import itemgetter as i
from functools import cmp_to_key


class User(db.Document):
    _id = db.StringField()
    email = db.StringField()
    password = db.StringField()
    pseudo = db.StringField()
    team = db.ListField()
    friends_list = db.ListField()
    money = db.IntField()
    players = db.ListField()
    date_created = db.DateTimeField(default=datetime.utcnow())
    
    
    def register(self):
        request_json = json.loads(request.data)
        self._id = uuid.uuid4().hex
        self.email = request_json["email"]
        self.password = pbkdf2_sha256.encrypt(request_json["password"])
        self.pseudo = request_json["pseudo"]
        self.team = []
        self.friends_list = []
        self.money = 600000
        self.players = []
        
        # Check for existing email address
        if User.objects(email=request_json["email"]):
            return jsonify({"error": "Email address already in use"}), 400
        
        return self._save()
    
    
    def _save(self):
        if self.save():
            return "", 200
        
        return jsonify({"error": "Signup failed"}), 400
    
    
    def get_user_by_id(self, _id):
        return User.objects(_id=_id).first()
    
    
    def signout(self):
        session.clear()
    
    
    def login(self):
        request_json = json.loads(request.data)
        user = User.objects(email=request_json["email"]).first()
        if user and pbkdf2_sha256.verify(request_json["password"], user.password):
            access_token = create_access_token(identity=user._id)
            print(access_token)
            return jsonify({"access_token": access_token}), 200
        return jsonify({"error": "Invalid login credentials"}), 401
    
    
    def get_money(self):
        return jsonify({"money": self.money}), 200
    
    
    def get_my_players(self, filters):
        _filters_true = []
        for key, value in filters.items():
            if value:
                _filters_true.append(key)
        print(_filters_true)
        if _filters_true:
            _to_return = multikeysort(self.players, _filters_true)
            return jsonify({"my_players": _to_return}), 200
        else:
            return jsonify({"my_players": self.players}), 200
    
    
    def sell_one_player(self):
        request_json = json.loads(request.data)
        name_player_to_add = request_json["sell_one_player"]
        _len_list_player = len(self.players)
        _index_player = 0
        _break = False
        while _index_player <= _len_list_player:
            if name_player_to_add == self.players[_index_player]['name']:
                self.money += int(self.players[_index_player]['price'])
                self.players.pop(_index_player)
                self.save()
                _break = True
                break
            _index_player += 1
        if _break:
            return self._save()
        else:
            return jsonify({"error": "Sell One Player Failed"}), 400

    def add_one_player(self):
        request_json = json.loads(request.data)
        name_player_to_add = request_json["add_one_player"]
        player = Player().get_one(name_player_to_add)
        if player:
            if player.get_price() > self.money:
                return jsonify({"error": "you don't have enough money"}), 400
            else:
                if player.to_json() in self.players:
                    return jsonify({"error": "You already have this player"}), 400
                self.players.append(player.to_json())
                self.money = self.money - player.get_price()
                return self._save()
        else:
            return jsonify({"error": "Add One Player Failed"}), 400


def cmp(x, y):
    return (x < y) - (x > y)


def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    
    
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    
    return sorted(items, key=cmp_to_key(comparer))