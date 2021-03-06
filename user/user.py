#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LeveilFlorian Enterprise, all rights reserved.

import json
import uuid
from _datetime import datetime
from functools import cmp_to_key
from operator import itemgetter as i

from flask import jsonify, request, session
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from database import db
from player.player import Player


class User(db.Document):
    _id = db.StringField()
    email = db.StringField()
    password = db.StringField()
    pseudo = db.StringField()
    my_team = db.DictField()
    friends_list = db.ListField()
    request_friends_list = db.ListField()
    waiting_friends_list = db.ListField()
    money = db.IntField()
    players = db.ListField()
    date_created = db.DateTimeField(default=datetime.utcnow())
    players_selected_by_position = db.DictField()
    
    
    def register(self):
        request_json = json.loads(request.data)
        self._id = uuid.uuid4().hex
        self.email = request_json["email"]
        self.password = pbkdf2_sha256.encrypt(request_json["password"])
        self.pseudo = request_json["pseudo"]
        self.my_team = {'GK': '', 'LB': '', 'RB': '', 'CB': '', 'MC': '', 'LM': '', 'RM': '', 'CAM': '', 'LW': '', 'RW': '', 'ST': ''}
        self.friends_list = []
        self.request_friends_list = []
        self.waiting_friends_list = []
        self.money = 600000
        self.players = []
        self.players_selected_by_position = {'GK': '', 'LB': '', 'RB': '', 'CB': '', 'MC': '', 'LM': '', 'RM': '', 'CAM': '', 'LW': '', 'RW': '', 'ST': ''}
        
        # Check for existing email address
        if User.objects(email=request_json["email"]):
            return jsonify({"error": "Email address already in use"}), 400
        
        return self.do_save()
    
    
    def get_player_instance():
        return Player()
    
    
    def do_save(self):
        if self.save():
            return "", 200
        
        return jsonify({"error": "Signup failed"}), 400
    
    
    def get_my_team(self):
        for key, value in self.players_selected_by_position.items():
            self.my_team[key] = Player().get_one(value)
        self.save()
        return self.my_team
    
    
    def get_friends_list(self):
        if self.friends_list:
            return jsonify({"_list": self.friends_list}), 200
        else:
            return jsonify({"error": "You don't have any friends"}), 400
    
    
    def get_waiting_friend_list(self):
        if self.waiting_friends_list:
            return jsonify({"_list": self.waiting_friends_list}), 200
        else:
            return jsonify({"error": "You didn't ask for friends"}), 400
    
    
    def get_request_friend_list(self):
        if self.request_friends_list:
            return jsonify({"_list": self.request_friends_list}), 200
        else:
            return jsonify({"error": "You have no friend request"}), 400
    
    
    def act_rm_friend_friend_list(self):
        request_json = json.loads(request.data)
        friend_email = request_json["user_email"]
        _copy_friends_list = self.friends_list.copy()
        for index, friend in enumerate(_copy_friends_list, start=0):
            if friend["email"] == friend_email:
                self.friends_list.pop(index)
                return self.do_save()
        return jsonify({"error": "Remove Friend In List Failed"}), 400
    
    
    def act_accept_friend_request_list(self):
        request_json = json.loads(request.data)
        friend_email = request_json["user_email"]
        _friend = self.get_user_by_email(friend_email)
        _copy_request_friends_list = self.request_friends_list.copy()
        for index, friend in enumerate(_copy_request_friends_list, start=0):
            if friend["email"] == friend_email:
                self.request_friends_list.pop(index)
                self.friends_list.append({'email': _friend.email, 'pseudo': _friend.pseudo})
                return self.do_save()
        return jsonify({"error": "Accept Friend Request List Failed"}), 400
    
    
    def act_refuse_friend_request_list(self):
        request_json = json.loads(request.data)
        friend_email = request_json["user_email"]
        _copy_request_friends_list = self.v.copy()
        for index, friend in enumerate(_copy_request_friends_list, start=0):
            if friend["email"] == friend_email:
                self.request_friends_list.pop(index)
                return self.do_save()
        return jsonify({"error": "Refuse Friend Request List Failed"}), 400
    
    
    def act_cancel_friend_waiting_list(self):
        request_json = json.loads(request.data)
        friend_email = request_json["user_email"]
        _copy_waiting_list = self.waiting_friends_list.copy()
        for index, friend in enumerate(_copy_waiting_list, start=0):
            if friend["email"] == friend_email:
                self.waiting_friends_list.pop(index)
                return self.do_save()
        return jsonify({"error": "Cancel Friend Waiting List Failed"}), 400
    
    
    def act_add_friend_waiting_list(self):
        request_json = json.loads(request.data)
        friend_email = request_json["user_email"]
        _friend = self.get_user_by_email(friend_email)
        if _friend:
            available, msg = self.check_available_friend_request(_friend.email)
            if not available:
                return jsonify({"error": msg}), 400
            self.waiting_friends_list.append({'email': _friend.email, 'pseudo': _friend.pseudo})
            _friend.request_friends_list.append({'email': self.email, 'pseudo': self.pseudo})
            _friend.do_save()
            return self.do_save()
        else:
            return jsonify({"error": "No user had this email address"}), 400
    
    
    def check_available_friend_request(self, _friend_email):
        if self.email == _friend_email:
            return False, "You cannot add yourself"
        elif _friend_email in [user["email"] for user in self.friends_list]:
            return False, "This user are in your friend list"
        elif _friend_email in [user["email"] for user in self.waiting_friends_list]:
            return False, "This user are in your waiting friend list"
        elif _friend_email in [user["email"] for user in self.request_friends_list]:
            return False, "This user are in your request friend list"
        else:
            return True, ""
    
    
    def get_user_by_id(self, _id):
        return User.objects(_id=_id).first()
    
    
    def get_user_by_email(self, _email):
        return User.objects(email=_email).first()
    
    
    def signout(self):
        session.clear()
    
    
    def login(self):
        request_json = json.loads(request.data)
        user = User.objects(email=request_json["email"]).first()
        if user and pbkdf2_sha256.verify(request_json["password"], user.password):
            access_token = create_access_token(identity=user._id)
            return jsonify({"access_token": access_token, "user_id": user._id}), 200
        return jsonify({"error": "Invalid login credentials"}), 401
    
    
    def get_money(self):
        return jsonify({"money": self.money}), 200
    
    
    def get_players_selected_by_position(self):
        return jsonify({"players_selected_by_position": self.players_selected_by_position}), 200
    
    
    def save_my_team(self):
        request_json = json.loads(request.data)
        _selected_players = request_json["_selected_players"]
        for key, value in _selected_players.items():
            if value in [player['name'] for player in self.players]:
                if self.my_team[key] and value != self.my_team[key].name:
                    self.my_team[key] = Player().get_one(value)
                if self.players_selected_by_position[key] != value:
                    self.players_selected_by_position[key] = value
            elif value == "":
                continue
            else:
                return jsonify({"error": "The players selected are not in list of my players."}), 401
        
        return self.do_save()
    
    
    def get_my_players(self, filters):
        _filters_true = []
        for key, value in filters.items():
            if value:
                _filters_true.append(key)
        if _filters_true:
            _to_return = multikeysort(self.players, _filters_true)
            return jsonify({"my_players": _to_return}), 200
        else:
            return jsonify({"my_players": self.players}), 200
    
    
    def get_one_of_my_players(self):
        request_json = json.loads(request.data)
        _selected_player = request_json["player_name"]
        if True if _selected_player in [my_player["name"] for my_player in self.players] else False:
            return jsonify({"player": player for player in self.players if player["name"] == _selected_player}), 200
        else:
            return jsonify({"error": "Get one player failed"}), 400
    
    
    def remove_player_in_selected_list_and_team(self, player_name):
        for key, value in self.players_selected_by_position.items():
            if value == player_name:
                self.players_selected_by_position[key] = ""
        
        for key, value in self.my_team.items():
            if value == player_name:
                self.my_team[key] = ""
    
    
    def sell_one_player(self):
        request_json = json.loads(request.data)
        name_player_to_add = request_json["sell_one_player"]
        _len_list_player = len(self.players)
        _index_player = 0
        _break = False
        while _index_player <= _len_list_player:
            if name_player_to_add == self.players[_index_player]['name']:
                if name_player_to_add in self.players_selected_by_position.values():
                    self.remove_player_in_selected_list_and_team(name_player_to_add)
                self.money += int(self.players[_index_player]['price'])
                self.players.pop(_index_player)
                self.save()
                _break = True
                break
            _index_player += 1
        if _break:
            return self.do_save()
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
                return self.do_save()
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
