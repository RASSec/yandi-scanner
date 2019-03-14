#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yds
# @Time    : 18-5-18
# @File    : subdomain_brute.py
# @Desc    : ""

import time
import os
from threading import Thread
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response, send_from_directory
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from yandi.views.authenticate import login_check
from yandi.views.modules.github import mgithub_brute

log = Blueprint('log', __name__)


@log.route('/log', methods=['POST', 'GET'])
@login_check
def log_view():
    if request.method == 'GET':
        return render_template('log.html')

