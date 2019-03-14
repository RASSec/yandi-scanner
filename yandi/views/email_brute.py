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
from yandi.views.modules.email import memail_brute

email_brute = Blueprint('email_brute', __name__)
email_db = db_name_conf()['mail_task_db']
subemail_db = db_name_conf()['mail_db']


@email_brute.route('/email-brute', methods=['POST', 'GET'])
@login_check
def email_view():
    if request.method == 'GET':
        # task delete
        if request.args.get('delete'):
            email_id = request.args.get('delete')
            connectiondb(email_db).delete_one({'_id': ObjectId(email_id)})
            connectiondb(subemail_db).remove({'email_id': ObjectId(email_id)})
            return redirect(url_for('email_brute.email_view'))

        # result download
        elif request.args.get('download'):
            email_id = request.args.get('download')
            try:
                file_name = connectiondb(email_db).find_one({'_id': ObjectId(email_id)})['email_name']
                file_path = os.getcwd() + '/yandi/static/download/'
                if os.path.exists(file_path + file_name):
                    os.remove(file_path + file_name)
                try:
                    for result in connectiondb(subemail_db).find({'email_id': ObjectId(email_id)}):
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
            email_data = connectiondb(email_db).find().sort('date', -1)
            return render_template('email-brute.html', email_data=email_data)

    # new domain
    elif request.method == 'POST':
        email_name_val = request.form.get('domain_name_val')
        payloads_val = request.form.get('domain_val').split('\n'),
        third_domain = request.form.get('third_domain')
        payloads_list = list(payloads_val)[0]
        if third_domain == "true":
            scan_option = 'Enable'
        else:
            scan_option = 'Disallow'
        email_data = {
            'email_name': email_name_val,
            'email_payloads': payloads_list,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'third_domain': scan_option,
            'status': "Preparation",
        }
        email_id = connectiondb(email_db).insert_one(email_data).inserted_id
        if email_id:
            # async domain brute
            t1 = Thread(target=memail_brute.start_email_brute, args=(email_name_val,payloads_list,email_id))
            t1.start()
            return "success"


@email_brute.route('/email-list', methods=['POST', 'GET'])
@login_check
def email_list():
    # Filter out the domain task
    if request.method == "GET":
        if request.args.get('domain'):
            email_id = request.args.get('domain')
            sub_result = connectiondb(subemail_db).find({'email_id': ObjectId(email_id)})
            return render_template('email-list.html', sub_result=sub_result)

        # return subdomain for poc scan
        elif request.args.get('subdomain'):
            subemail = []
            email_id = request.args.get('subdomain')
            for i in connectiondb(subemail_db).find({'email_id': ObjectId(email_id)}):
                subemail.append(i['subemail'])
            return '\n'.join(subemail)

        # delete subdomain
        elif request.args.get('delete'):
            subemail_id = request.args.get('delete')
            email_id = connectiondb(subemail_db).find_one({'_id': ObjectId(subemail_id)})['email_id']
            result = connectiondb(subemail_db).delete_one({'_id': ObjectId(subemail_id)})
            if result:
                return redirect(url_for('email_brute.email_list', domain=email_id))

        # default view
        else:
            sub_result = connectiondb(subemail_db).find()
            return render_template('email-list.html', sub_result=sub_result)

