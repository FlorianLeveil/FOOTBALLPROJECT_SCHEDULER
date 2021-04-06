#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
# This file is part of Shinken Enterprise, all rights reserved.
from scheduler import app
from user.user import User


@app.route('/user/register', methods=['POST'])
def register():
    return User().register()


@app.route('/user/signout')
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()
