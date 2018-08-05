#!/usr/bin/python3
# coding=utf-8

import time
import urllib.request
from bs4 import BeautifulSoup
import sys
import re
import datetime
import json
import syslog


# 指定した記事を開き，取り消し済みならNoneを返す
def urlopen(url):
	try:
		resp = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		return None
	else:
		return resp

# readyfor
url = 'https://readyfor.jp/tags/'

# ページの情報を取得
resp = urllib.request.urlopen(url)

src = resp.read()
soup = BeautifulSoup(src, 'lxml')

# 地域タグ
tags = soup.find_all("li", class_="tag region")

for tag in tags:
	print("region," + tag.text)

# テーマタグ
tags = soup.find_all("li", class_="tag")

# 地域タグも混じるので排除
for tag in tags:
	if len(tag.get('class')) == 1:
		print("theme," + tag.text)
