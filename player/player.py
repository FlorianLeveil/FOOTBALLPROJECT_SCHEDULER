#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LeveilFlorian Enterprise, all rights reserved.

from flask import jsonify

from database import db


class Player(db.Document):
    name = db.StringField()
    foot = db.StringField()
    position = db.StringField()
    league = db.StringField()
    price = db.IntField()
    age = db.IntField()
    height = db.IntField()
    overall = db.IntField()
    crossing = db.IntField()
    finishing = db.IntField()
    short_passing = db.IntField()
    volleys = db.IntField()
    dribbling = db.IntField()
    curve = db.IntField()
    long_passing = db.IntField()
    ball_control = db.IntField()
    acceleration = db.IntField()
    sprint_speed = db.IntField()
    agility = db.IntField()
    reactions = db.IntField()
    balance = db.IntField()
    shot_power = db.IntField()
    strength = db.IntField()
    long_shots = db.IntField()
    aggression = db.IntField()
    interceptions = db.IntField()
    positioning = db.IntField()
    vision = db.IntField()
    penalties = db.IntField()
    marking = db.IntField()
    standing_tackle = db.IntField()
    sliding_tackle = db.IntField()
    gk_diving = db.IntField()
    gk_handling = db.IntField()
    gk_kicking = db.IntField()
    gk_positioning = db.IntField()
    gk_reflexes = db.IntField()
    
    
    def to_json(self, just_int=False):
        to_return = {
            'price'          : self.price,
            'age'            : self.age,
            'height'         : self.height,
            'overall'        : self.overall,
            'crossing'       : self.crossing,
            'finishing'      : self.finishing,
            'short_passing'  : self.short_passing,
            'volleys'        : self.volleys,
            'dribbling'      : self.dribbling,
            'curve'          : self.curve,
            'long_passing'   : self.long_passing,
            'ball_control'   : self.ball_control,
            'acceleration'   : self.acceleration,
            'sprint_speed'   : self.sprint_speed,
            'agility'        : self.agility,
            'reactions'      : self.reactions,
            'balance'        : self.balance,
            'shot_power'     : self.shot_power,
            'strength'       : self.strength,
            'long_shots'     : self.long_shots,
            'aggression'     : self.aggression,
            'interceptions'  : self.interceptions,
            'positioning'    : self.positioning,
            'vision'         : self.vision,
            'penalties'      : self.penalties,
            'marking'        : self.marking,
            'standing_tackle': self.standing_tackle,
            'sliding_tackle' : self.sliding_tackle,
            'gk_diving'      : self.gk_diving,
            'gk_handling'    : self.gk_handling,
            'gk_kicking'     : self.gk_kicking,
            'gk_positioning' : self.gk_positioning,
            'gk_reflexes'    : self.gk_reflexes,
        }
        
        if not just_int:
            string_to_return = {
                'name'    : self.name,
                'foot'    : self.foot,
                'position': self.position,
                'league'  : self.league,
            }
            to_return.update(string_to_return)
        return to_return
    
    
    def __repr__(self):
        return '{' + self.name + ', ' + self.foot + ', ' + self.position + ', ' + self.league + ', ' + str(self.price) + ', ' + str(self.age) + ', ' + str(self.height) + ', ' + str(self.overall) + ', ' + str(self.crossing) + ', ' + str(
            self.finishing) + ', ' + str(self.short_passing) + ', ' + str(self.volleys) + ', ' + str(self.dribbling) + ', ' + str(self.curve) + ', ' + str(self.long_passing) + ', ' + str(self.ball_control) + ', ' + str(
            self.acceleration) + ', ' + str(self.sprint_speed) + ', ' + str(self.agility) + ', ' + str(self.reactions) + ', ' + str(self.balance) + ', ' + str(self.shot_power) + ', ' + str(self.strength) + ', ' + str(self.long_shots) + ', ' + str(
            self.aggression) + ', ' + str(self.interceptions) + ', ' + str(self.positioning) + ', ' + str(self.vision) + ', ' + str(self.penalties) + ', ' + str(self.marking) + ', ' + str(self.standing_tackle) + ', ' + str(
            self.sliding_tackle) + ', ' + str(self.gk_diving) + ', ' + str(self.gk_handling) + ', ' + str(self.gk_kicking) + ', ' + str(self.gk_positioning) + ', ' + str(self.gk_reflexes) + '}'
    
    
    def get_one(self, name):
        player = Player.objects(name=name).first()
        if player:
            return player
        else:
            return None
    
    
    def get_price(self):
        return self.price
    
    
    def get_all(self, start, end, filters):
        _filters_true = []
        for key, value in filters.items():
            if value:
                if key == "name" or key == "league":
                    _filters_true.append(key)
                    continue
                _filters_true.append('-' + key)
        if start and end:
            players = Player.objects.order_by(*_filters_true)[start:end]
        elif start:
            players = Player.objects.order_by(*_filters_true)[start:]
        elif end:
            players = Player.objects.order_by(*_filters_true)[:end]
        else:
            players = Player.objects()
        if players:
            to_result = []
            for player in players:
                to_result.append(player.to_json())
            return jsonify({"players": to_result}), 200
        else:
            return jsonify({"error": " Bad Request"}), 400
