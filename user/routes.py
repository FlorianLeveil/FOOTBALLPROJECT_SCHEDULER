#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2021:
# This file is part of LeveilFlorian Enterprise, all rights reserved.
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from scheduler import app
from user.user import User


@app.route('/user/register', methods=['POST'])
def register():
    return User().register()


@app.route('/user/signout')
@jwt_required()
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()


@app.route('/user/get_money')
@jwt_required()
def get_money():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.get_money()


@app.route('/user/get_players_selected_by_position')
@jwt_required()
def get_players_selected_by_position():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.get_players_selected_by_position()


@app.route('/user/add_one_player', methods=['POST'])
@jwt_required()
def add_one_player():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.add_one_player()


@app.route('/user/sell_one_player', methods=['POST'])
@jwt_required()
def sell_one_player():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.sell_one_player()


@app.route('/user/save_my_team', methods=['POST'])
@jwt_required()
def save_my_team():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.save_my_team()


@app.route('/user/get_one_of_my_players', methods=['POST'])
@jwt_required()
def get_one_of_my_players():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.get_one_of_my_players()


@app.route('/user/get_my_players')
@jwt_required()
def get_my_players():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    filters = {'name'          : request.args.get('name', default=False, type=bool), 'foot': request.args.get('foot', default=False, type=bool), 'position': request.args.get('position', default=False, type=bool),
               'league'        : request.args.get('league', default=False, type=bool), 'price': request.args.get('price', default=False, type=bool), 'age': request.args.get('age', default=False, type=bool),
               'height'        : request.args.get('height', default=False, type=bool),
               'overall'       : request.args.get('overall', default=False, type=bool), 'crossing': request.args.get('crossing', default=False, type=bool), 'finishing': request.args.get('finishing', default=False, type=bool),
               'short_passing' : request.args.get('short_passing', default=False, type=bool), 'volleys': request.args.get('volleys', default=False, type=bool), 'dribbling': request.args.get('dribbling', default=False, type=bool),
               'curve'         : request.args.get('curve', default=False, type=bool), 'long_passing': request.args.get('long_passing', default=False, type=bool), 'ball_control': request.args.get('ball_control', default=False, type=bool),
               'acceleration'  : request.args.get('acceleration', default=False, type=bool), 'sprint_speed': request.args.get('sprint_speed', default=False, type=bool), 'agility': request.args.get('agility', default=False, type=bool),
               'reactions'     : request.args.get('reactions', default=False, type=bool), 'balance': request.args.get('balance', default=False, type=bool), 'shot_power': request.args.get('shot_power', default=False, type=bool),
               'strength'      : request.args.get('strength', default=False, type=bool), 'long_shots': request.args.get('long_shots', default=False, type=bool), 'aggression': request.args.get('aggression', default=False, type=bool),
               'interceptions' : request.args.get('interceptions', default=False, type=bool), 'positioning': request.args.get('positioning', default=False, type=bool), 'vision': request.args.get('vision', default=False, type=bool),
               'penalties'     : request.args.get('penalties', default=False, type=bool), 'marking': request.args.get('marking', default=False, type=bool), 'standing_tackle': request.args.get('standing_tackle', default=False, type=bool),
               'sliding_tackle': request.args.get('sliding_tackle', default=False, type=bool), 'gk_diving': request.args.get('gk_diving', default=False, type=bool), 'gk_handling': request.args.get('gk_handling', default=False, type=bool),
               'gk_kicking'    : request.args.get('gk_kicking', default=False, type=bool), 'gk_positioning': request.args.get('gk_positioning', default=False, type=bool), 'gk_reflexes': request.args.get('gk_reflexes', default=False, type=bool)}
    return user.get_my_players(filters)


@app.route('/user/get_friends_list')
@jwt_required()
def get_friends_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.get_friends_list()


@app.route('/user/get_waiting_friend_list')
@jwt_required()
def get_waiting_friend_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.get_waiting_friend_list()


@app.route('/user/get_request_friend_list')
@jwt_required()
def get_request_friend_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.get_request_friend_list()


@app.route('/user/act_rm_friend_friend_list', methods=['POST'])
@jwt_required()
def act_rm_friend_friend_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.act_rm_friend_friend_list()


@app.route('/user/act_accept_friend_request_list', methods=['POST'])
@jwt_required()
def act_accept_friend_request_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.act_accept_friend_request_list()


@app.route('/user/act_refuse_friend_request_list', methods=['POST'])
@jwt_required()
def act_refuse_friend_request_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.act_refuse_friend_request_list()


@app.route('/user/act_cancel_friend_waiting_list', methods=['POST'])
@jwt_required()
def act_cancel_friend_waiting_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.act_cancel_friend_waiting_list()


@app.route('/user/act_add_friend_waiting_list', methods=['POST'])
@jwt_required()
def act_add_friend_waiting_list():
    current_user_id = get_jwt_identity()
    user = User().get_user_by_id(current_user_id)
    return user.act_add_friend_waiting_list()
