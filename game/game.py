#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
# This file is part of LeveilFlorian Enterprise, all rights reserved.
import random
import threading
import time


class WEIGHT_ATTACK_STAT(object):
    def __init__(self):
        self.AGE = 10
        self.HEIGHT = 10
        self.OVERALL = 10
        self.AGILITY = 12
        self.DRIBBLING = 15
        self.BALANCE = 7
        self.BALL_CONTROL = 15
        self.SPRINT_SPEED = 13
        self.ACCELERATION = 13
        self.CROSSING = 7
    
    
    def get_weight(self):
        return {
            'age'         : self.AGE,
            'height'      : self.HEIGHT,
            'overall'     : self.OVERALL,
            'agility'     : self.AGILITY,
            'dribbling'   : self.DRIBBLING,
            'balance'     : self.BALANCE,
            'ball_control': self.BALL_CONTROL,
            'sprint_speed': self.SPRINT_SPEED,
            'acceleration': self.ACCELERATION,
            'crossing'    : self.CROSSING,
        }


class WEIGHT_DEFENSE_STAT(object):
    def __init__(self):
        self.AGE = 10
        self.HEIGHT = 10
        self.OVERALL = 10
        self.AGILITY = 12
        self.DRIBBLING = 14
        self.INTERCEPTIONS = 14
        self.MARKING = 14
        self.STANDING_TACKLE = 14
        self.SLIDING_TACKLE = 14
    
    
    def get_weight(self):
        return {
            'age'            : self.AGE,
            'height'         : self.HEIGHT,
            'overall'        : self.OVERALL,
            'agility'        : self.AGILITY,
            'dribbling'      : self.DRIBBLING,
            'interceptions'  : self.INTERCEPTIONS,
            'marking'        : self.MARKING,
            'standing_tackle': self.STANDING_TACKLE,
            'sliding_tackle' : self.SLIDING_TACKLE,
        }


class WEIGHT_SHOOT_STAT(object):
    def __init__(self):
        self.AGE = 10
        self.HEIGHT = 10
        self.OVERALL = 7
        self.BALANCE = 10
        self.FINISHING = 15
        self.LONG_SHOTS = 12
        self.SHOT_POWER = 15
        self.VOLLEYS = 15
        self.CURVE = 15
    
    
    def get_weight(self):
        return {
            'age'       : self.AGE,
            'height'    : self.HEIGHT,
            'overall'   : self.OVERALL,
            'balance'   : self.BALANCE,
            'finishing' : self.FINISHING,
            'long_shots': self.LONG_SHOTS,
            'shot_power': self.SHOT_POWER,
            'volleys'   : self.VOLLEYS,
            'curve'     : self.CURVE,
        }


class WEIGHT_GK_STAT(object):
    def __init__(self):
        self.AGE = 10
        self.HEIGHT = 10
        self.OVERALL = 7
        self.BALANCE = 10
        self.GK_DIVING = 15
        self.GK_HANDLING = 15
        self.GK_KICKING = 12
        self.GK_POSITIONING = 15
        self.GK_REFLEXES = 15
    
    
    def get_weight(self):
        return {
            'age'           : self.AGE,
            'height'        : self.HEIGHT,
            'overall'       : self.OVERALL,
            'balance'       : self.BALANCE,
            'gk_diving'     : self.GK_DIVING,
            'gk_handling'   : self.GK_HANDLING,
            'gk_kicking'    : self.GK_KICKING,
            'gk_positioning': self.GK_POSITIONING,
            'gk_reflexes'   : self.GK_REFLEXES,
        }


class WEIGHT_SHORT_PASS(object):
    def __init__(self):
        self.SHORT_PASSING = 10
        self.POSITIONING = 7
    
    
    def get_weight(self):
        return {
            'short_passing': self.SHORT_PASSING,
            'positioning'  : self.POSITIONING,
            
        }


class WEIGHT_LONG_PASS(object):
    def __init__(self):
        self.VISION = 7
        self.STRENGTH = 10
        self.LONG_PASSING = 7
    
    
    def get_weight(self):
        return {
            'vision'      : self.VISION,
            'strength'    : self.STRENGTH,
            'long_passing': self.LONG_PASSING,
        }


class ADVERSE_POSITION(object):
    # GK and CB cannot fail !
    LB = 'LW'
    RB = 'RW'
    MC = 'CAM'
    LM = 'LM'
    RM = 'RM'
    CAM = 'MC'
    LW = 'LB'
    RW = 'RB'
    ST = 'GK'


class POSITION_GIVE_TO_POSITION(object):
    GK = {'SHORT': ['LB', 'RB'], 'MEDIUM': ['MC', 'LM'], 'LONG': ['CAM']}
    LB = {'SHORT': ['CB'], 'MEDIUM': ['MC'], 'LONG': ['LM']}
    RB = {'SHORT': ['CB'], 'MEDIUM': ['MC'], 'LONG': ['RM']}
    CB = {'SHORT': ['MC'], 'MEDIUM': [''], 'LONG': ['LM', 'RM']}
    MC = {'SHORT': ['LM', 'RM'], 'MEDIUM': ['CAM'], 'LONG': ['']}
    LM = {'SHORT': ['MC'], 'MEDIUM': ['CAM'], 'LONG': ['LW']}
    RM = {'SHORT': ['MC'], 'MEDIUM': ['CAM'], 'LONG': ['RW']}
    CAM = {'SHORT': ['LW', 'RW'], 'MEDIUM': [''], 'LONG': ['ST']}
    LW = {'SHORT': ['ST'], 'MEDIUM': ['SHOOT'], 'LONG': ['RW']}
    RW = {'SHORT': ['ST'], 'MEDIUM': ['SHOOT'], 'LONG': ['LW']}
    ST = {'SHORT': ['SHOOT']}


class Game(threading.Thread):
    def __init__(self, game_id, redis_client, player1_id, player2_id, player1_team, player2_team):
        threading.Thread.__init__(self)
        
        # PLAYER PROPS
        self.game_id = game_id
        self.redis = redis_client
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_team = player1_team
        self.player2_team = player2_team
        
        # INTERNAL VALUE
        self._weight_attack = WEIGHT_ATTACK_STAT().get_weight()
        self._weight_defense = WEIGHT_DEFENSE_STAT().get_weight()
        self._total_weight_attack_defense = 112
        self._weight_shoot = WEIGHT_SHOOT_STAT().get_weight()
        self._weight_gk = WEIGHT_GK_STAT().get_weight()
        self._total_weight_shoot_gk = 109
        self._weight_short_pass = WEIGHT_SHORT_PASS().get_weight()
        self._total_weight_short_pass = 17
        self._weight_long_pass = WEIGHT_LONG_PASS().get_weight()
        self._total_weight_long_pass = 24
        self._percent_max_short_pass = 45
        self._percent_max_long_pass = 20
        
        # CURRENT VALUE IN MATCH
        self.player1_have_ball = False
        self.player_with_ball_position = 'MC'
        self.time_match = 0
        self.end = False
        self.winner = ""
        self.player1_score = 0
        self.player2_score = 0
        self.running = False
    
    
    def save(self):
        _save = {
            "end"                      : str(self.end),
            "winner"                   : str(self.winner),
            "time_match"               : str(self.time_match),
            "player_with_ball_position": str(self.player_with_ball_position),
            "player1_id"               : str(self.player1_id),
            "player2_id"               : str(self.player2_id),
            "player1_have_ball"        : str(self.player1_have_ball),
            "player1_score"            : str(self.player1_score),
            "player2_score"            : str(self.player2_score)
        }
        
        self.redis.hmset(self.game_id, _save)
    
    
    def stop(self):
        self.running = False
    
    
    def run(self):
        self.compute_which_player_start()
        self.running = True
        self.save()
        while self.running:
            self.save()
            time.sleep(1)
            _position_to_give = self.compute_position_to_give(self.player_with_ball_position)
            _success_action = self.compute_success_of_action(_position_to_give)
            self.set_position_after_action(_success_action, _position_to_give)
            self.time_match += 1
            if self.time_match == 90:
                self.end = True
                self.winner = self.compute_winner()
                self.save()
                self.running = False
    
    
    def compute_winner(self):
        if self.player1_score == self.player2_score:
            return 'NULL'
        elif self.player1_score > self.player2_score:
            return self.player1_id
        else:
            return self.player2_id
    
    
    def compute_position_to_give(self, current_position_player):
        _position_to_return = 'SHOOT'
        if current_position_player == 'ST':
            return _position_to_return
        _dict_of_position_to_give = getattr(POSITION_GIVE_TO_POSITION, current_position_player)
        _player_with_ball = self.player2_team[self.player_with_ball_position]
        _weight_short_pass, _weight_long_pass = self.compute_pass_with_weight(_player_with_ball)
        
        _can_short_pass, _can_medium_pass, _can_long_pass = self.compute_which_pass_is_possible(_dict_of_position_to_give)
        _type_of_pass_compute = self.compute_pass_type(_can_short_pass, _can_medium_pass, _can_long_pass, _weight_short_pass, _weight_long_pass)
        _position_to_return = random.choice(_dict_of_position_to_give[_type_of_pass_compute])
        return _position_to_return
    
    
    @staticmethod
    def compute_pass_type(can_short_pass, can_medium_pass, can_long_pass, weight_short_pass, weight_long_pass):
        _short = 'SHORT'
        _medium = 'MEDIUM'
        _long = 'LONG'
        _random_number = random.randrange(101)
        
        if can_short_pass and can_medium_pass and can_long_pass:
            _medium_pass_percent = 100 - weight_short_pass - weight_long_pass
            if _random_number >= _medium_pass_percent + weight_short_pass:
                return _long
            elif _random_number >= weight_short_pass:
                return _medium
            else:
                return _short
        elif can_short_pass and can_medium_pass:
            if _random_number >= weight_short_pass:
                return _medium
            else:
                return _short
        else:
            # it s short and long pass
            if _random_number >= weight_long_pass:
                return _long
            else:
                return _short
    
    
    @staticmethod
    def compute_which_pass_is_possible(dict_of_position_to_give):
        _can_short_pass = False
        _can_medium_pass = False
        _can_long_pass = False
        
        for pass_type, to_position in dict_of_position_to_give.items():
            if pass_type == 'SHORT' and to_position != ['']:
                _can_short_pass = True
            elif pass_type == 'MEDIUM' and to_position != ['']:
                _can_medium_pass = True
            elif pass_type == 'LONG' and to_position != ['']:
                _can_long_pass = True
            else:
                continue
        
        return _can_short_pass, _can_medium_pass, _can_long_pass
    
    
    def compute_pass_with_weight(self, player_with_ball):
        _weight_short_pass = self._compute_pass_weight(player_with_ball, self._weight_short_pass, self._total_weight_short_pass, self._percent_max_short_pass)
        _weight_long_pass = self._compute_pass_weight(player_with_ball, self._weight_long_pass, self._total_weight_long_pass, self._percent_max_long_pass)
        return _weight_short_pass, _weight_long_pass
    
    
    @staticmethod
    def _compute_pass_weight(player_with_ball, weight_stat, total_weight, percent_max):
        _value_to_return = 0
        for key, weight in weight_stat.items():
            _player_stat = getattr(player_with_ball, key)
            _value_to_return += (_player_stat * weight)
        
        _to_return = int((_value_to_return * percent_max) / (total_weight * 4))
        return _to_return
    
    
    def compute_success_of_action(self, position_to_give):
        # GK and CB cannot fail !
        _action_was_success = True
        if self.player_with_ball_position == 'GK' or self.player_with_ball_position == 'CB':
            return _action_was_success
        
        if position_to_give == 'SHOOT':
            if self.player1_have_ball:
                _player_with_ball = self.player1_team[self.player_with_ball_position]
                _player_opponent = self.player2_team['GK']
            else:
                _player_with_ball = self.player2_team[self.player_with_ball_position]
                _player_opponent = self.player1_team['GK']
            
            _attack_power, _defense_power = self.compute_power_with_weight(_player_with_ball, _player_opponent, self._weight_shoot, self._weight_gk, self._total_weight_shoot_gk)
        
        else:
            if self.player1_have_ball:
                _player_with_ball = self.player1_team[self.player_with_ball_position]
                _player_opponent = self.player2_team[getattr(ADVERSE_POSITION, self.player_with_ball_position)]
            else:
                _player_with_ball = self.player2_team[self.player_with_ball_position]
                _player_opponent = self.player1_team[getattr(ADVERSE_POSITION, self.player_with_ball_position)]
            _attack_power, _defense_power = self.compute_power_with_weight(_player_with_ball, _player_opponent, self._weight_attack, self._weight_defense, self._total_weight_attack_defense)
        
        _chance_to_cross_defense = self._compute_chance_crossing(_attack_power, _defense_power)
        _action_was_success = random.randrange(101) <= _chance_to_cross_defense
        return _action_was_success
    
    
    @staticmethod
    def _compute_chance_crossing(attack_power, defense_power):
        return int(50 + (attack_power - defense_power))
    
    
    def compute_power_with_weight(self, player_with_ball, player_opponent, weight_attack, weight_defense, total_weight):
        _attack_power = self._compute_power(player_with_ball, weight_attack, total_weight)
        _defense_power = self._compute_power(player_opponent, weight_defense, total_weight)
        return _attack_power, _defense_power
    
    
    @staticmethod
    def _compute_power(player_with_ball, weight_stat, total_weight):
        _value_to_return = 0
        for key, weight in weight_stat.items():
            _player_stat = getattr(player_with_ball, key)
            _value_to_return += (_player_stat * weight)
        
        _to_return = (_value_to_return * 100) / (total_weight * 4)
        return _to_return
    
    
    def compute_which_player_start(self):
        self.player1_have_ball = random.choice([True, False])
    
    
    def set_position_after_action(self, action_success, position_to_give):
        if action_success:
            if position_to_give == 'SHOOT':
                if self.player1_have_ball:
                    self.player1_score += 1
                else:
                    self.player2_score += 1
                self.player1_have_ball = not self.player1_have_ball
                self.player_with_ball_position = 'MC'
                self.save()
                time.sleep(4)
            else:
                self.player_with_ball_position = position_to_give
        
        else:
            self.player1_have_ball = not self.player1_have_ball
            self.player_with_ball_position = getattr(ADVERSE_POSITION, self.player_with_ball_position)
