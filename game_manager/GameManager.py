#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
# This file is part of LeveilFlorian Enterprise, all rights reserved.
import threading
import time
import uuid
from math import floor

from flask import jsonify

from game.game import Game
from player.player import Player
from user.user import User


class GameManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.games = []
        self.user = User()
        self.player = Player()
        GameManagerParsing(self.redis).start()
        GameManagerInitGame(self.redis, self.user).start()
    
    
    def add_player_to_queue(self, user_id):
        _user = self.user.get_user_by_id(user_id)
        _player_team = _user.get_my_team()
        for value in _player_team.values():
            if value == '':
                return jsonify({"error": "You'r team is not complete, you cannot play !"}), 400
        
        self.redis.rpush('queue', user_id)
        return jsonify({"add_to_queue": "True"}), 200
    
    
    def get_an_opponent(self, user_id):
        game_id = self.redis.get(user_id)
        if game_id:
            return jsonify({"game_id": str(game_id)[2:-1]}), 200
        else:
            return jsonify({"game_id": "no_game"}), 200
    
    
    def get_my_game(self, game_id):
        dict_of_byte = self.redis.hgetall(game_id)
        new_dict = {}
        for key, value in dict_of_byte.items():
            new_dict[str(key)[2:-1]] = str(value)[2:-1]
        return jsonify({"game": new_dict}), 200
    
    
    def get_all_teams(self, player1_id, player2_id):
        _user_1 = self.user.get_user_by_id(player1_id)
        _user_2 = self.user.get_user_by_id(player2_id)
        _player_team1 = _user_1.get_my_team()
        _player_team2 = _user_2.get_my_team()
        return jsonify({"team": {"team1": _player_team1, "team2": _player_team2}}), 200
    
    
    def play_with_a_ia(self, user_id):
        _game_id = uuid.uuid4().hex
        _player_1_id = user_id
        _player_2_id = '0000000'
        _user_1 = self.user.get_user_by_id(user_id)
        _player_1_team = _user_1.get_my_team()
        for value in _player_1_team.values():
            if value == '':
                return jsonify({"error": "You'r team is not complete, you cannot play !"}), 400
        _player_2_team = IATeam(self.player).Team
        Game(_game_id, self.redis, _player_1_id, _player_2_id, _player_1_team, _player_2_team).start()
        return jsonify({"game_id_with_ia": _game_id, "team1": _player_1_team, "team2": _player_2_team}), 200
    
    
    def delete_game(self, user_id, game_id):
        self.redis.delete(user_id)
        self.redis.delete(game_id)
        return "", 201


class GameManagerParsing(threading.Thread):
    def __init__(self, redis_client):
        threading.Thread.__init__(self)
        self.redis = redis_client
    
    
    def run(self):
        while True:
            time.sleep(1)
            _list_users_id = self.redis.lrange("queue", 0, -1)
            _number_of_needed_iteration = floor(len(_list_users_id) / 2)
            _iteration_number = 0
            if _number_of_needed_iteration >= 1:
                while _iteration_number < _number_of_needed_iteration:
                    _player_1 = _list_users_id[_iteration_number]
                    _player_2 = _list_users_id[_iteration_number + 1]
                    
                    self.redis.lrem("queue", 1, _player_1)
                    self.redis.lrem("queue", 1, _player_2)
                    
                    _game_id = uuid.uuid4().hex
                    self.redis.set(_player_1, _game_id)
                    self.redis.set(_player_2, _game_id)
                    self.redis.hmset(_game_id, {"player1_id": _player_1, "player2_id": _player_2})
                    self.redis.rpush('game_to_start', _game_id)
                    _iteration_number += 2


class GameManagerInitGame(threading.Thread):
    def __init__(self, redis_client, user):
        threading.Thread.__init__(self)
        self.redis = redis_client
        self.user = user
    
    
    def run(self):
        while True:
            time.sleep(1)
            _list_games_to_start = self.redis.lrange("game_to_start", 0, -1)
            if len(_list_games_to_start) >= 1:
                for _game_id in _list_games_to_start:
                    _game = self.redis.hgetall(_game_id)
                    self.redis.lrem("game_to_start", 1, _game_id)
                    _player_1_id = str(_game[b"player1_id"])
                    _player_2_id = str(_game[b"player2_id"])
                    _user_1 = self.user.get_user_by_id(_player_1_id[2:-1])
                    _user_2 = self.user.get_user_by_id(_player_2_id[2:-1])
                    _player_1_team = _user_1.get_my_team()
                    _player_2_team = _user_2.get_my_team()
                    Game(_game_id, self.redis, _player_1_id[2:-1], _player_2_id[2:-1], _player_1_team, _player_2_team).start()


class IATeam(object):
    def __init__(self, player):
        self.Player1 = player.get_one('Alphonse Areola')
        self.Player2 = player.get_one('Lucas Digne')
        self.Player3 = player.get_one('Serge Aurier')
        self.Player4 = player.get_one('Aymen Abdennour')
        self.Player5 = player.get_one('Geoffrey Kondogbia')
        self.Player6 = player.get_one('Raphael Guerreiro')
        self.Player7 = player.get_one('Bernardo Silva')
        self.Player8 = player.get_one('Fares Bahlouli')
        self.Player9 = player.get_one('Paul-Georges Ntep')
        self.Player10 = player.get_one('Romain Hamouma')
        self.Player11 = player.get_one('Anthony Martial')
        self.Team = {'GK': self.Player1, 'LB': self.Player2, 'RB': self.Player3, 'CB': self.Player4, 'MC': self.Player5, 'LM': self.Player6, 'RM': self.Player7, 'CAM': self.Player8, 'LW': self.Player9, 'RW': self.Player10, 'ST': self.Player11}
