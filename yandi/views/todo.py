#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yds
# @Time    : 18-5-15
# @File    : dashboard.py
# @Desc    : ""

import datetime
import re
from collections import Counter
from flask import Blueprint, render_template
from bson import ObjectId
from lib.mongo_db import connectiondb, db_name_conf
from yandi.views.authenticate import login_check
from flask import Blueprint, render_template, request
from instance import config_name



todo = Blueprint('todo', __name__)
config_db = db_name_conf()['config_db']


@todo.route('/todo', methods=['GET', 'POST'])
@login_check
def view_todo():
    if request.method == "GET":
        config_data = connectiondb(config_db).find_one({"config_name": config_name})
        config_info = {
            "todotext": config_data['todo'],
        }
        return render_template("todo.html", config_info=config_info)
    else:
        # update thread config
        if request.form.get("source") == "todo":
            update_config = {
                "todo": request.form.get('todotext')
            }
            if connectiondb(config_db).update_one({'config_name': config_name}, {"$set": update_config}):
                return "success"
            else:
                return "Warning"
