#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LeveilFlorian Enterprise, all rights reserved.
import time

from game.game import Game
from scheduler import db, redis_client
from flask import Flask, jsonify, request, json


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



User_1_Player1 = Player().get_one('Anthony Lopes')
User_1_Player2 = Player().get_one('Layvin Kurzawa')
User_1_Player3 = Player().get_one('Fabinho')
User_1_Player4 = Player().get_one('Marquinhos')
User_1_Player5 = Player().get_one('Marco Verratti')
User_1_Player6 = Player().get_one('Andre Ayew')
User_1_Player7 = Player().get_one('Florian Thauvin')
User_1_Player8 = Player().get_one('Nabil Fekir')
User_1_Player9 = Player().get_one('Yannick Ferreira Carrasco')
User_1_Player10 = Player().get_one('Lucas Ocampos')
User_1_Player11 = Player().get_one('Alexandre Lacazette')

team1 = {'GK': User_1_Player1, 'LB': User_1_Player2, 'RB': User_1_Player3, 'CB': User_1_Player4, 'MC': User_1_Player5, 'LM': User_1_Player6, 'RM': User_1_Player7, 'CAM': User_1_Player8, 'LW': User_1_Player9, 'RW': User_1_Player10, 'ST': User_1_Player11}


User_2_Player1 = Player().get_one('Alphonse Areola')
User_2_Player2 = Player().get_one('Lucas Digne')
User_2_Player3 = Player().get_one('Serge Aurier')
User_2_Player4 = Player().get_one('Aymen Abdennour')
User_2_Player5 = Player().get_one('Geoffrey Kondogbia')
User_2_Player6 = Player().get_one('Raphael Guerreiro')
User_2_Player7 = Player().get_one('Bernardo Silva')
User_2_Player8 = Player().get_one('Fares Bahlouli')
User_2_Player9 = Player().get_one('Paul-Georges Ntep')
User_2_Player10 = Player().get_one('Romain Hamouma')
User_2_Player11 = Player().get_one('Anthony Martial')

team2 = {'GK': User_2_Player1, 'LB': User_2_Player2, 'RB': User_2_Player3, 'CB': User_2_Player4, 'MC': User_2_Player5, 'LM': User_2_Player6, 'RM': User_2_Player7, 'CAM': User_2_Player8, 'LW': User_2_Player9, 'RW': User_2_Player10, 'ST': User_2_Player11}




game = Game('toto', redis_client, '1', '2', team1, team2)
game2 = Game('2', redis_client, 3, 4, team1, team2)
game3 = Game('3', redis_client, 5, 6, team1, team2)
game4 = Game('4', redis_client, 7, 8, team1, team2)

game.start()
# game4.start()
# game2.start()
# game3.start()

while True:
    print(redis_client.hgetall('toto'))
    time.sleep(1)

# player.name,
# player.foot,
# player.position,
# player.league,
# player.age,
# player.height,
# player.overall,
# player.crossing,
# player.finishing,
# player.short_passing,
# player.volleys,
# player.dribbling,
# player.curve,
# player.long_passing,
# player.ball_control,
# player.acceleration,
# player.sprint_speed,
# player.agility,
# player.reactions,
# player.balance,
# player.shot_power,
# player.strength,
# player.long_shots,
# player.aggression,
# player.interceptions,
# player.positioning,
# player.vision,
# player.penalties,
# player.marking,
# player.standing_tackle,
# player.sliding_tackle,
# player.gk_diving,
# player.gk_handling,
# player.gk_kicking,
# player.gk_positioning,
# player.gk_reflexes,
#
#
#
# item.get_node("name").text = name
# item.get_node("foot").text = foot
# item.get_node("position").text = position
# item.get_node("league").text = league
# item.get_node("age").text = age
# item.get_node("height").text = height
# item.get_node("overall").text = overall
# item.get_node("crossing").text = crossing
# item.get_node("finishing").text = finishing
# item.get_node("short_passing").text = short_passing
# item.get_node("volleys").text = volleys
# item.get_node("dribbling").text = dribbling
# item.get_node("curve").text = curve
# item.get_node("long_passing").text = long_passing
# item.get_node("ball_control").text = ball_control
# item.get_node("acceleration").text = acceleration
# item.get_node("sprint_speed").text = sprint_speed
# item.get_node("agility").text = agility
# item.get_node("reactions").text = reactions
# item.get_node("balance").text = balance
# item.get_node("shot_power").text = shot_power
# item.get_node("strength").text = strength
# item.get_node("long_shots").text = long_shots
# item.get_node("aggression").text = aggression
# item.get_node("interceptions").text = interceptions
# item.get_node("positioning").text = positioning
# item.get_node("vision").text = vision
# item.get_node("penalties").text = penalties
# item.get_node("marking").text = marking
# item.get_node("standing_tackle").text = standing_tackle
# item.get_node("sliding_tackle").text = sliding_tackle
# item.get_node("gk_diving").text = gk_diving
# item.get_node("gk_handling").text = gk_handling
# item.get_node("gk_kicking").text = gk_kicking
# item.get_node("gk_positioning").text = gk_positioning
# item.get_node("gk_reflexes").text = gk_reflexes


# item.get_node("age").text = age as String
# item.get_node("height").text = height as String
# item.get_node("overall").text = overall as String
# item.get_node("crossing").text = crossing as String
# item.get_node("finishing").text = finishing as String
# item.get_node("short_passing").text = short_passing as String
# item.get_node("volleys").text = volleys as String
# item.get_node("volleys").text = volleys as String
# item.get_node("dribbling").text = dribbling as String
# item.get_node("curve").text = curve as String
# item.get_node("long_passing").text = long_passing as String
# item.get_node("ball_control").text = ball_control as String
# item.get_node("acceleration").text = acceleration as String
# item.get_node("sprint_speed").text = sprint_speed as String
# item.get_node("agility").text = agility as String
# item.get_node("reactions").text = reactions as String
# item.get_node("balance").text = balance as String
# item.get_node("shot_power").text = shot_power as String
# item.get_node("strength").text = strength as String
# item.get_node("long_shots").text = long_shots as String
# item.get_node("aggression").text = aggression as String
# item.get_node("interceptions").text = interceptions as String
# item.get_node("positioning").text = positioning as String
# item.get_node("vision").text = vision as String
# item.get_node("penalties").text = penalties as String
# item.get_node("marking").text = marking as String
# item.get_node("standing_tackle").text = standing_tackle as String
# item.get_node("sliding_tackle").text = sliding_tackle as String
# item.get_node("gk_diving").text = gk_diving as String
# item.get_node("gk_handling").text = gk_handling as String
# item.get_node("gk_kicking").text = gk_kicking as String
# item.get_node("gk_positioning").text = gk_positioning as String
# item.get_node("gk_reflexes").text = gk_reflexes as String
