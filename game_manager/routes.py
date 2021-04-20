#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
 # This file is part of LeveilFlorian Enterprise, all rights reserved.

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from game_manager import GameManager
from scheduler import app, game_manager
from user.user import User


@app.route('/game_manager/get_request_friend_list')
@jwt_required()
def get_request_friend_list():
    current_user_id = get_jwt_identity()
    return game_manager.add_to_queue(current_user_id)
