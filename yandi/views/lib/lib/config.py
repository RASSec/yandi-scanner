#coding:utf-8
#Author:se55i0n

import re
import os
import sys
import sqlite3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


#User-Agent
agent = {'UserAgent':'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))'}

#re
rtitle   = re.compile(r'title="(.*)"')
rheader  = re.compile(r'header="(.*)"')
rbody    = re.compile(r'body="(.*)"')
rbracket = re.compile(r'\((.*)\)')

path = os.path.dirname(os.path.abspath(__file__))

#中文乱码及ssl错误
def setting():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check(_id):
	with sqlite3.connect(path +'/web.db') as conn:
		cursor = conn.cursor()
		result = cursor.execute('SELECT name, keys FROM `fofa` WHERE id=\'{}\''.format(_id))
		for row in result:
			return row[0], row[1]

def count():
	with sqlite3.connect(path + '/web.db') as conn:
		cursor = conn.cursor()
		result = cursor.execute('SELECT COUNT(id) FROM `fofa`')
		for row in result:
			return row[0]
