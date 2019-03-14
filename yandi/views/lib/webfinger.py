#!/usr/bin/env python
#coding:utf-8
import re
import sys
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
from lib.config import *

class Cmsscanner(object):
	def __init__(self, target):
		self.target = target
		self.start  = time.time()
		self.re=[]
		setting()

	def get_info(self):
		"""获取web的信息"""
		try:
			r = requests.get(url=self.target, headers=agent, 
				timeout=3, verify=False)
			content = r.text
			try:
				title = BeautifulSoup(content, 'lxml').title.text.strip()
				return str(r.headers), content, title.strip('\n')
			except:
				return str(r.headers), content, ''
		except Exception as e:
			pass

	def check_rule(self, key, header, body, title):
		"""指纹识别"""
		try:
			if 'title="' in key:
				if re.findall(rtitle, key)[0].lower() in title.lower():
					return True
			elif 'body="' in key:
				if re.findall(rbody, key)[0] in body:return True
			else:
				if re.findall(rheader, key)[0] in header:return True
		except Exception as e:
			pass

	def handle(self, _id, header, body, title):
		"""取出数据库的key进行匹配"""
		result_success = []
		name, key = check(_id)
		#满足一个条件即可的情况
		if '||' in key and '&&' not in key and '(' not in key:
			for rule in key.split('||'):
				if self.check_rule(rule, header, body, title):
					#print '%s   %s' %(self.target, name)
					result_success.append(name)
					break
		#只有一个条件的情况
		elif '||' not in key and '&&' not in key and '(' not in key:
			if self.check_rule(key, header, body, title):
				#print '%s   %s' %(self.target, name)
				result_success.append(name)
		#需要同时满足条件的情况
		elif '&&' in key and '||' not in key and '(' not in key:
			num = 0
			for rule in key.split('&&'):
				if self.check_rule(rule, header, body, title):
					num += 1
			if num == len(key.split('&&')):
				#print '%s   %s' %(self.target, name)
				result_success.append(name)
		else:
			#与条件下存在并条件: 1||2||(3&&4)
			if '&&' in re.findall(rbracket, key)[0]:
				for rule in key.split('||'):
					if '&&' in rule:
						num = 0
						for _rule in rule.split('&&'):
							if self.check_rule(_rule, header, body, title):
								num += 1
						if num == len(rule.split('&&')):
							#print '%s   %s' %(self.target, name)
							result_success.append(name)
							break
					else:
						if self.check_rule(rule, header, body, title):
							#print '%s   %s' %(self.target, name)
							result_success.append(name)
							break
			else:
				#并条件下存在与条件： 1&&2&&(3||4)
				for rule in key.split('&&'):
					num = 0
					if '||' in rule:
						for _rule in rule.split('||'):
							if self.check_rule(_rule, title, body, header):
								num += 1
								break
					else:
						if self.check_rule(rule, title, body, header):
							num += 1
				if num == len(key.split('&&')):
					#print '%s   %s' %(self.target, name)
					result_success.append(name)
		test1=[i for i in result_success if i != '']
		if test1[0] != '':
			return '\n'.join(test1)
	def run(self):

		try:
			header, body, title = self.get_info()
			for _id in xrange(1, int(count())):
				try:
					self.re.append(self.handle(_id, header, body, title))
				except Exception as e:
					pass
		except Exception as e:
			print e
		return self.re
			#print u'%s[+] 指纹识别完成, 耗时 %s 秒.%s' %(O, time.time()-self.start, W)

def openmain(target,subdomain_id):
	target_url = "http://" + target
	result = {
		"webfinder": Cmsscanner(target_url).run(),
		"_id": subdomain_id
	}
	return result