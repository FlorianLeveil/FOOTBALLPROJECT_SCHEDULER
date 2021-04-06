#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019:
# This file is part of Shinken Enterprise, all rights reserved.

import json
import uuid
from _datetime import datetime
from flask import jsonify, request, session
from passlib.hash import pbkdf2_sha256
from scheduler import db


class User(db.Document):
    _id = db.StringField()
    email = db.StringField()
    password = db.StringField()
    pseudo = db.StringField()
    team = db.ListField()
    friends_list = db.ListField()
    money = db.IntField()
    players = db.ListField()
    date_created = db.DateTimeField(default=datetime.utcnow())
    
    
    def start_session(self):
        session['logged_in'] = True
        session['user'] = self
        return jsonify(self), 200
    
    
    def register(self):
        request_json = json.loads(request.data)
        self._id = uuid.uuid4().hex
        self.email = request_json["email"]
        self.password = pbkdf2_sha256.encrypt(request_json["password"])
        self.pseudo = request_json["pseudo"]
        self.team = []
        self.friends_list = []
        self.money = 15000
        self.players = []
        
        # Check for existing email address
        if User.objects(email=request_json["email"]):
            return jsonify({"error": "Email address already in use"}), 400
        
        if self.save():
            return self.start_session()
        
        return jsonify({"error": "Signup failed"}), 400
    
    
    def signout(self):
        session.clear()
    
    
    def login(self):
        request_json = json.loads(request.data)
        user = User.objects(email=request_json["email"]).first()
        if user and pbkdf2_sha256.verify(request_json["password"], user.password):
            return self.start_session()
        
        return jsonify({"error": "Invalid login credentials"}), 401
    