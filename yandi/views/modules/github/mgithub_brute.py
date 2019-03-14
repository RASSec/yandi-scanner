#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yds
# @Time    : 18-5-19
# @File    : domain_brute.py
# @Desc    : ""

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
github_db = db_name_conf()['github_db']
subgithub_db = db_name_conf()['subgithub_db']
config_db = db_name_conf()['config_db']

class githubBrute:

    def __init__(self, github_name_val,payloads_list, github_id):
        print("[*] %s %s Brute Start" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), github_id))
        self.keyword=github_name_val
        self.github = payloads_list
        self.github_id = github_id
        self.third_domain = connectiondb(github_db).find_one({"_id": github_id})['third_domain']
        self.resolver_ip = ''
        self.result = ''


    def multi_brute(self):
        g_User = connectiondb(config_db).find_one({"config_name": config_name})['github_user']
        g_Pass = connectiondb(config_db).find_one({"config_name": config_name})['github_password']
        keyword = self.keyword
        payloads = self.github
        sensitive_list = []
        comp_list = []
        data_save=[]
        tUrls = []
        login_url = 'https://github.com/login'
        session_url = 'https://github.com/session'
        try:
            s = requests.session()
            resp = s.get(login_url).text
            dom_tree = etree.HTML(resp)
            key = dom_tree.xpath('//input[@name="authenticity_token"]/@value')
            # print key
            user_data = {
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': key,
                'login': g_User,
                'password': g_Pass
            }
            # print key,g_User,g_Pass
            s.post(session_url, data=user_data)
            s.get('https://github.com/settings/profile')
            # print g_User,g_Pass
        except Exception as e:
            print e
        try:
            print('login.......')
            sleep(1)
            for page in tqdm(range(1, connectiondb(config_db).find_one({"config_name": config_name})['github_page'])):
                search_code = 'https://github.com/search?p=' + str(page) + '&q=' + keyword + '&type=Code'
                resp = s.get(search_code)
                results_code = resp.text
                dom_tree_code = etree.HTML(results_code)
                Urls = dom_tree_code.xpath('//div[@class="flex-auto min-width-0 col-10"]/a[2]/@href')
                users = dom_tree_code.xpath('//div[@class="flex-auto min-width-0 col-10"]/a[1]/text()')
                datetime = dom_tree_code.xpath('//relative-time/text()')
                filename = dom_tree_code.xpath('//div[@class="flex-auto min-width-0 col-10"]/a[2]/text()')
                for i in range(len(Urls)):
                    for Url in Urls:
                        Url = 'https://github.com' + Url
                        tUrls.append(Url)
                        #[,filename[i]]
                    data = {
                        "subgithub": self.keyword,
                        "github": self.github,
                        "github_id": self.github_id,
                        "date": datetime[i],
                        "result": tUrls[i],
                        "user":users[i],
                        "title": '',
                    }
                    data_save.append(data)
                try:
                    if data_save:
                        connectiondb(subgithub_db).insert_many(data_save, ordered=True)
                except Exception as e:
                    print(e)
            print  sensitive_list, comp_list
        except Exception as e:
            print(e)


def start_github_brute(github_name_val,payloads_list, github_id):
    time_start = datetime.now()
    print("[*] %s Domain Brute start %s" % (time_start.strftime("%Y-%m-%d %H:%M:%S"), github_id))
    connectiondb(github_db).update_one({"_id": github_id}, {"$set": {
        "status": "Running"
    }})
    start_brute = githubBrute(github_name_val,payloads_list, github_id)
    start_brute.multi_brute()
    connectiondb(github_db).update_one({"_id": github_id}, {"$set": {
        "status": "Done"
    }})
    time_end = datetime.now()
    print("[*] %s Domain Brute Done %s" % (time_end.strftime("%Y-%m-%d %H:%M:%S"), github_id))
    print("[*] %s Used Time: %s" % (time_end.strftime("%Y-%m-%d %H:%M:%S"), (time_end - time_start).seconds))