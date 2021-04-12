# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LeveilFlorian Enterprise, all rights reserved.
import csv

from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db'  : 'scheduler',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

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

with open('./data.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in data:
        player = Player()
        player.name = row[0]
        player.foot = row[1]
        player.position = row[2]
        player.league = row[3]
        player.age = int(row[4])
        player.height = int(row[5])
        player.overall = int(row[6])
        player.crossing = int(row[7])
        player.finishing = int(row[8])
        player.short_passing = int(row[9])
        player.volleys = int(row[10])
        player.dribbling = int(row[11])
        player.curve = int(row[12])
        player.long_passing = int(row[13])
        player.ball_control = int(row[14])
        player.acceleration = int(row[15])
        player.sprint_speed = int(row[16])
        player.agility = int(row[17])
        player.reactions = int(row[18])
        player.balance = int(row[19])
        player.shot_power = int(row[20])
        player.strength = int(row[21])
        player.long_shots = int(row[22])
        player.aggression = int(row[23])
        player.interceptions = int(row[24])
        player.positioning = int(row[25])
        player.vision = int(row[26])
        player.penalties = int(row[27])
        player.marking = int(row[28])
        player.standing_tackle = int(row[29])
        player.sliding_tackle = int(row[30])
        player.gk_diving = int(row[31])
        player.gk_handling = int(row[32])
        player.gk_kicking = int(row[33])
        player.gk_positioning = int(row[34])
        player.gk_reflexes = int(row[35])
        player.save()


players = Player.objects()
for player in players:
    total_point = 0
    
    for value in player.to_json(True).values():
        total_point += int(value)
    
    player.price = total_point * 1000
    player.save()
    
print('Good')


