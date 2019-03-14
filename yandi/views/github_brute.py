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

github_brute = Blueprint('gitub_brute', __name__)
github_db = db_name_conf()['github_db']
subgithub_db = db_name_conf()['subgithub_db']


@github_brute.route('/github-brute', methods=['POST', 'GET'])
@login_check
def github_view():
    if request.method == 'GET':
        # task delete
        if request.args.get('delete'):
            github_id = request.args.get('delete')
            connectiondb(github_db).delete_one({'_id': ObjectId(github_id)})
            connectiondb(subgithub_db).remove({'github_id': ObjectId(github_id)})
            return redirect(url_for('github_brute.github_view'))

        # result download
        elif request.args.get('download'):
            github_id = request.args.get('download')
            try:
                file_name = connectiondb(github_db).find_one({'_id': ObjectId(github_id)})['github_name']
                file_path = os.getcwd() + '/yandi/static/download/'
                if os.path.exists(file_path + file_name):
                    os.remove(file_path + file_name)
                try:
                    for result in connectiondb(subgithub_db).find({'github_id': ObjectId(github_id)}):
                        with open(file_path + file_name, "a") as download_file:
                            download_file.write(result['result'] + "\n")
                    sub_response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
                    sub_response.headers["Content-Disposition"] = "attachment; filename=" + file_name
                    return sub_response
                except Exception as e:
                    return e
            except Exception as e:
                print(e)
        else:
            github_data = connectiondb(github_db).find().sort('date', -1)
            return render_template('github-brute.html', github_data=github_data)

    # new domain
    elif request.method == 'POST':
        github_name_val = request.form.get('domain_name_val')
        payloads_val = request.form.get('domain_val').split('\n'),
        third_domain = request.form.get('third_domain')
        payloads_list = list(payloads_val)[0]
        if third_domain == "true":
            scan_option = 'Enable'
        else:
            scan_option = 'Disallow'
        github_data = {
            'github_name': github_name_val,
            'github_payloads': payloads_list,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'third_domain': scan_option,
            'status': "Preparation",
        }
        github_id = connectiondb(github_db).insert_one(github_data).inserted_id
        if github_id:
            # async domain brute
            t1 = Thread(target=mgithub_brute.start_github_brute, args=(github_name_val,payloads_list,github_id))
            t1.start()
            return "success"


@github_brute.route('/github-list', methods=['POST', 'GET'])
@login_check
def github_list():
    # Filter out the domain task
    if request.method == "GET":
        if request.args.get('domain'):
            github_id = request.args.get('domain')
            sub_result = connectiondb(subgithub_db).find({'github_id': ObjectId(github_id)})
            return render_template('github-list.html', sub_result=sub_result)

        # return subdomain for poc scan
        elif request.args.get('subdomain'):
            subgithub = []
            github_id = request.args.get('subdomain')
            for i in connectiondb(subgithub_db).find({'github_id': ObjectId(github_id)}):
                subgithub.append(i['subgithub'])
            return '\n'.join(subgithub)

        # delete subdomain
        elif request.args.get('delete'):
            subgithub_id = request.args.get('delete')
            github_id = connectiondb(subgithub_db).find_one({'_id': ObjectId(subgithub_id)})['github_id']
            result = connectiondb(subgithub_db).delete_one({'_id': ObjectId(subgithub_id)})
            if result:
                return redirect(url_for('github_brute.github_list', domain=github_id))

        # default view
        else:
            sub_result = connectiondb(subgithub_db).find()
            return render_template('github-list.html', sub_result=sub_result)

