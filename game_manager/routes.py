#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
# This file is part of LeveilFlorian Enterprise, all rights reserved.

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from scheduler import game_manager, app


@app.route('/gamemanager/play_with_a_ia')
@jwt_required()
def play_with_a_ia():
    current_user_id = get_jwt_identity()
    return game_manager.play_with_a_ia(current_user_id)


@app.route('/gamemanager/get_my_game')
@jwt_required()
def get_my_game():
    game_id = request.args.get('game_id', default='', type=str)
    return game_manager.get_my_game(game_id)


@app.route('/gamemanager/add_player_to_queue')
@jwt_required()
def add_player_to_queue():
    current_user_id = get_jwt_identity()
    return game_manager.add_player_to_queue(current_user_id)


@app.route('/gamemanager/get_an_opponent')
@jwt_required()
def get_an_opponent():
    current_user_id = get_jwt_identity()
    return game_manager.get_an_opponent(current_user_id)


@app.route('/gamemanager/get_all_teams')
@jwt_required()
def get_all_teams():
    _id_player_1 = request.args.get('player1_id', default='', type=str)
    _id_player_2 = request.args.get('player2_id', default='', type=str)
    return game_manager.get_all_teams(_id_player_1, _id_player_2)


@app.route('/gamemanager/delete_game')
@jwt_required()
def delete_game():
    current_user_id = get_jwt_identity()
    game_id = request.args.get('game_id', default='', type=str)
    return game_manager.delete_game(current_user_id, game_id)
