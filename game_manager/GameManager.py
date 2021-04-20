#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
 # This file is part of LeveilFlorian Enterprise, all rights reserved.
import uuid

from flask import jsonify

from game.game import Game


class GameManager:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.mongo = db
        self.games = []
    
    
    def add_player_to_queue(self, user_id):
        self.redis.rpush('queue', user_id)
    
    
    def get_an_opponent(self, user_id):
        index = 0
        game_id = self.redis.get(user_id)
        if game_id:
            return jsonify({"game_id": game_id}), 200
        
        while index != self.redis.llen('queue'):
            if user_id == self.redis.lindex('queue', index):
                if self.redis.llen('queue') >= 2:
                    _game_id = uuid.uuid4().hex
                    if index != 0:
                        player_enemy_id = self.redis.lpop('queue')
                    else:
                        player_enemy_id = self.redis.rpop('queue')
                    self.redis.set(player_enemy_id, _game_id)
                    self.redis.set(user_id, _game_id)
                    self.redis.lrem('queue', index)
                    return jsonify({"game_id": _game_id}), 200
            index += 1
        return jsonify({"error": "Waiting an opponent."}), 400
    
    
    def get_my_game(self, game_id):
        return jsonify({"game": self.redis.hgetall(game_id)}), 200
    
    
    def start_game(self, game_id):
        if game_id in self.games:
            return "", 200
        game = Game(game_id, self.redis, 1,1,1,1)
        self.games.append(game)
        game.start()
        return "", 200
    
    
    
    def get_info(self, game_id):
        return jsonify({"game": self.redis.get(game_id)}), 200
